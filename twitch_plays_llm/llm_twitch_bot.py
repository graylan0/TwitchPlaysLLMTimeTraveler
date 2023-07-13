GameHooks

class LlmTwitchBot(commands.Bot):
    """
    Twitch bot for the AI Dungeon game.

    Args:
        game: The game instance.
    """

    def __init__(self, game: LlmGame):
        super().__init__(
            irc_token=config.twitch_bot_username,
            client_id=config.twitch_bot_client_id,
            nick=config.twitch_bot_username,
            prefix='!',
            initial_channels=[config.twitch_channel_name],
        )
        self.game = game

    async def event_ready(self):
        """Called when the bot has successfully connected to the server."""
        print(f'We are logged in as {self.nick}')

    async def event_message(self, message):
        """Called when a message is posted in the chat."""
        print(message.content)
        await self.handle_commands(message)

    @commands.command(name='start')
    async def start_game(self, ctx):
        """Starts the game."""
        self.game.restart()
        await ctx.send(self.game.initial_story_message)

    @commands.command(name='propose')
    async def propose_action(self, ctx, *, proposal: str):
        """Proposes an action for the main character to take."""
        proposal_id = self.game.add_proposal(proposal, ctx.author.name)
        await ctx.send(f'Proposal #{proposal_id} added: {proposal}')

    @commands.command(name='vote')
    async def vote(self, ctx, proposal_id: int):
        """Votes for a proposal."""
        try:
            proposal = self.game.vote(proposal_id)
            await ctx.send(f'Vote added to proposal #{proposal_id}: {proposal.message}')
        except ValueError:
            await ctx.send(f'Invalid proposal id: {proposal_id}')

    @commands.command(name='endvote')
    async def end_vote(self, ctx):
        """Ends the voting process."""
        self.game.end_vote()

class LlmTwitchBotHooks(LlmGameHooks):
    """
    Twitch bot hooks for the AI Dungeon game.

    Args:
        channel: The Twitch channel.
    """

    def __init__(self, channel: Channel):
        self.channel = channel

    async def on_get_narration_result(self, narration_result: str, proposal: Proposal, proposal_id: int):
        """Sends the narration result to the chat."""
        await self.channel.send(f'Proposal #{proposal_id + 1} by {proposal.user} won: {proposal.message}')
        await self.channel.send(narration_result)

def main():
    """Main function to start the bot."""
    bot = LlmTwitchBot(LlmGame(LlmTwitchBotHooks(bot._ws._channel_cache[config.twitch_channel_name])))
    bot.run()

if __name__ == '__main__':
    main()
