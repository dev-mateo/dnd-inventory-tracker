from discord import app_commands, Interaction, Embed, Color
from discord.ext import commands
from asyncio import sleep

class Purge(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="purge",
        description="Mass delete messages"
    )
    @app_commands.describe(
        amount="The amount of messages you want to delete"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def purge(self, interaction: Interaction, amount: int) -> None:

        await interaction.response.send_message("Purging...")
        await interaction.channel.purge(limit=amount+1)

        embed = Embed(
            title="Success",
            description=f"{interaction.user.mention} has purged {amount} messages",
            color=Color.green()
        )
        success = await interaction.channel.send(embed=embed)
        await sleep(5)
        await success.delete()


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Purge(bot))
