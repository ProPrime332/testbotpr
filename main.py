from discord.ext import commands
import discord
from config import token, initial_cogs


from aiohttp import ClientSession
import datetime
import asyncio


class Helper(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(command_prefix=kwargs.pop('command_prefix', ['*']), case_insensitive=True, **kwargs)
        self.session = ClientSession(loop=self.loop)
        self.start_time = datetime.datetime.utcnow()
        self.clean_text = commands.clean_content(escape_markdown=True, fix_channel_mentions=True)

    """"  Events  """

    async def on_ready(self):
        print(f'Successfully logged in as {self.user}\nSharded to {len(self.guilds)} guilds')
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name=f'use the prefix *'))
        for ext in initial_cogs:
            self.load_extension(ext)

    @classmethod
    async def setup(cls, **kwargs):
        bot = cls()
        try:
            await bot.start(token, **kwargs)
        except KeyboardInterrupt:
            await bot.close()


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(Helper.setup())