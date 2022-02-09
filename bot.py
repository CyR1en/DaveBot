import logging

import discord
from discord import Colour
from discord.ext import commands
from discord.ext.commands import MissingRequiredArgument

from cog.misc import Misc
from cog.tracker import Tracker
from configuration import ConfigNode

logger = logging.getLogger(__name__)


class Bot(commands.Bot):
    def __init__(self, config_file, color=Colour.from_rgb(15, 185, 177), **options):
        super().__init__(config_file.get_tuple_node(ConfigNode.PREFIX), **options)
        self.color = color
        self.config_file = config_file
        self.token = None
        self.remove_command('help')
        self.add_cog(Tracker(self))

    async def on_ready(self):
        await self.change_presence(status=discord.Status.do_not_disturb, activity=discord.Game("with IBM"))
        logger.info('Successfully logged in as {}'.format(self.user))

    async def on_command_error(self, context, exception):
        if isinstance(exception, MissingRequiredArgument):
            await context.channel.send("You're missing an argument there")
            return
        raise exception

    def start_bot(self):
        self.run(self.config_file.get(ConfigNode.TOKEN))
