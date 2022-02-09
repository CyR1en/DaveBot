import logging

from discord.ext import commands

from cog.misc import Misc
from configuration import ConfigNode

logger = logging.getLogger(__name__)


class Tracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.config = bot.config_file
        self.color = bot.color

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        channel = message.channel
        tracked = self.config.get_dict_node(ConfigNode.TRACKED)
        if message.content not in tracked.keys():
            return
        tracked[message.content]["count"] = tracked[message.content]["count"] + 1
        self.config.set(ConfigNode.TRACKED, tracked)
        await channel.send(tracked[message.content]["response"].format(count=tracked[message.content]["count"]))

    @commands.group()
    async def tracker(self, ctx):
        if ctx.invoked_subcommand is None:
            await ctx.send(embed=Misc.build_help_embed(self))

    @tracker.command()
    async def add(self, ctx, *args):
        response = args[1]
        if "{count}" not in response:
            await ctx.send('The response is missing the `{count}` placeholder')
            return
        new_dict = {'count': 0, 'response': response}
        tracked_dict = self.config.get_dict_node(ConfigNode.TRACKED)
        tracked_dict[args[0]] = new_dict
        self.config.set(ConfigNode.TRACKED, tracked_dict)
        await ctx.send(f'Added `{args[0]}`')

    @tracker.command(name='edit-response')
    async def edit(self, ctx, key: str, response: str):
        tracked_dict = self.config.get_dict_node(ConfigNode.TRACKED)
        if key not in tracked_dict.keys():
            await ctx.send(f'The key `{key}` is not tracked')
            return
        if "{count}" not in response:
            await ctx.send('The response is missing the `{count}` placeholder')
            return
        tracked_dict[key]['response'] = response
        self.config.set(ConfigNode.TRACKED, tracked_dict)
        await ctx.send(f'Response for `{key}` changed!')

