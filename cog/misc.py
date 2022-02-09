import discord
from discord.ext import commands

from configuration import ConfigNode


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.color = bot.color
        self.config = bot.config_file

    @commands.command()
    async def help(self, ctx):
        await ctx.send(embed=Misc.build_help_embed(self))

    @staticmethod
    def build_help_embed(self):
        prefix = format(self.config.get_tuple_node(ConfigNode.PREFIX)[0])
        embed = discord.Embed(title="Here's what you could ask me to do", color=self.color)
        sample = """
                  {}tracker **add** "!key" "something {{count}} times"
                  """.format(prefix)
        edit_response = """
                  {}tracker **edit-response** <key> "new_response"
                  """.format(prefix)
        embed.add_field(name="To make a new tracker", value=sample, inline=False)
        embed.add_field(name="To edit tracker's response", value=edit_response, inline=False)

        embed.set_footer(text="Brought to you by IBM")
        return embed
