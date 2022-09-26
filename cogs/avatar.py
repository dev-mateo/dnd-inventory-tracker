from discord import app_commands, Interaction, Embed, Member
from discord.ext import commands


class Avatar(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="avatar",
        description="Get a user's avatar"
    )
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def avatar(self, interaction: Interaction, user: Member) -> None:
        embed = Embed(
            title="Avatar",
            description=f"{user.mention}'s avatar"
        )
        embed.set_image(url=user.avatar)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Avatar(bot))
