class CharacterMemory:
    MAX_PAST_ACTIONS = 100  # maximum number of past actions to store in memory
    PAST_ACTIONS_FILE = "past_actions.txt"  # file to store older actions

    def __init__(self):
        self.attributes = {}
        self.past_actions = []
        self.color_code = "white"  # default color
        self.profile = CharacterProfile("John Doe", 40, "Detective", ["Investigation", "Hand-to-hand combat"], {"Sarah": "Wife", "Tom": "Partner"})
        self.thoughts_file = "thoughts.txt"

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

    def add_past_action(self, action):
        self.past_actions.append(action)
        if len(self.past_actions) > self.MAX_PAST_ACTIONS:
            oldest_action = self.past_actions.pop(0)  # remove the oldest action
            with open(self.PAST_ACTIONS_FILE, "a") as file:
                file.write(oldest_action + "\n")  #...
