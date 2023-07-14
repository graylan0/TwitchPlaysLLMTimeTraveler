import bisect
import time
from collections import deque
from dataclasses import dataclass
from typing import List, Dict
import os
from pathlib import Path

@dataclass
class CharacterProfile:
    name: str
    age: int
    occupation: str
    skills: List[str]
    relationships: Dict[str, str]

class Memory:
    def __init__(self, content, priority=0):
        self.content = content
        self.priority = priority
        self.timestamp = time.time()

class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None
        self.prev = None

class TriDeque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.middle = None
        self.size = 0

    def add_left(self, data):
        node = Node(data)
        if self.head is None:
            self.head = self.tail = self.middle = node
        else:
            node.next = self.head
            self.head.prev = node
            self.head = node
            if self.size % 2 != 0:
                self.middle = self.middle.prev
        self.size += 1

    def add_middle(self, data):
        if self.head is None:
            self.add_left(data)
        else:
            node = Node(data)
            if self.size % 2 == 0:
                node.prev = self.middle
                node.next = self.middle.next
                self.middle.next.prev = node
                self.middle.next = node
            else:
                node.prev = self.middle.prev
                node.next = self.middle
                self.middle.prev.next = node
                self.middle.prev = node
            self.middle = node
            self.size += 1

    def add_right(self, data):
        node = Node(data)
        if self.head is None:
            self.head = self.tail = self.middle = node
        else:
            node.prev = self.tail
            self.tail.next = node
            self.tail = node
            if self.size % 2 == 0:
                self.middle = self.middle.next
        self.size += 1

    def remove_left(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is not None:
            self.head.prev = None
        else:
            self.tail = self.middle = None
        if self.size % 2 == 0:
            self.middle = self.middle.next
        self.size -= 1
        return data

    def remove_middle(self):
        if self.middle is None:
            return None
        data = self.middle.data
        if self.middle.prev is not None:
            self.middle.prev.next = self.middle.next
        if self.middle.next is not None:
            self.middle.next.prev = self.middle.prev
        if self.size % 2 == 0:
            self.middle = self.middle.next
        else:
            self.middle = self.middle.prev
        self.size -= 1
        return data

    def remove_right(self):
        if self.tail is None:
            return None
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail is not None:
            self.tail.next = None
        else:
            self.head = self.middle = None
        if self.size % 2 != 0:
            self.middle = self.middle.prev
        self.size -= 1
        return data

class CharacterMemory:
    MAX_PAST_ACTIONS = 100  # maximum number of past actions to store in memory
    PAST_ACTIONS_FILE = os.path.join(os.path.dirname(__file__), 'datafiles', 'past_actions.txt')  # file to store older actions

    def __init__(self):
        self.attributes = {}
        self.past_actions = TriDeque()  # Initialize a TriDeque
        self.color_code = "white"  # default color
        self.profile = CharacterProfile("John Doe", 40, "Detective", ["Investigation", "Hand-to-hand combat"], {"Sarah": "Wife", "Tom": "Partner"})
        self.thoughts_file = "thoughts.txt"

        # Check if the past actions file exists, and create it if it doesn't
        past_actions_path = Path(self.PAST_ACTIONS_FILE)
        past_actions_path.parent.mkdir(parents=True, exist_ok=True)  # Create the directory if it doesn't exist
        past_actions_path.touch(exist_ok=True)  # Create the file if it doesn't exist

    def update_attribute(self, attribute, value):
        self.attributes[attribute] = value
        if attribute == "mood":
            self.update_color_code(value)

    def update_color_code(self, mood):
        if mood == "happy":
            self.color_code = "yellow"
        elif mood == "sad":
            self.color_code = "blue"
        elif mood == "angry":
            self.color_code = "red"
        else:
            self.color_code = "white"

    def add_past_action(self, action, priority=0):
        memory = Memory(action, priority)
        self.past_actions.push(memory)

