url = 'https://api.quotable.io/random'

from discord import app_commands, Interaction
from discord.ext import commands
import requests

class Quote(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="quote",
        description="Get a random quote"
    )
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def ping(self, interaction: Interaction) -> None:
        data = requests.get(url).json()
        await interaction.response.send_message("\""+data["content"]+"\"" + " - " + data["author"])
        


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Quote(bot))
