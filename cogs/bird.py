from discord import app_commands, Interaction, Embed
from discord.ext import commands
import requests

API = "https://some-random-api.ml/animal/birb"


class Bird(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="bird",
        description="BIRD"
    )
    async def bird(self, interaction: Interaction) -> None:
        data = requests.get(API).json()

        embed = Embed(
            title="Bird",
            description=data["fact"]
        )
        embed.set_image(url=data["image"])

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Bird(bot))
