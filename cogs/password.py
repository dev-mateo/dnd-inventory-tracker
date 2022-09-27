from discord import app_commands, Interaction
from discord.ext import commands
import secrets, string

letters = string.ascii_letters
digits = string.digits
special_chars = string.punctuation
alphabet = letters + digits + special_chars

class Password(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="password",
        description="Generate a strong password"
    )
    @app_commands.describe(
        length="The length of the password",
    )
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def password(self, interaction: Interaction, length: int) -> None:
        pwd = ""
        for i in range(int(length)):
          pwd += "".join(secrets.choice(alphabet))

        await interaction.response.send_message(pwd, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Password(bot))
