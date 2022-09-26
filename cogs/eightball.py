from discord import app_commands, Interaction, Embed, Color
from discord.ext import commands
from random import choice
from datetime import datetime, timezone


class EightBall(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(
        name="8ball",
        description="Ask the 8ball a question"
    )
    @app_commands.describe(
        question="The question you're asking"
    )
    async def eightball(self, interaction: Interaction, question: str) -> None:

        choices = [
            "🟢 It is decidedly so.",
            "🟢 Without a doubt.",
            "🟢 Yes definitely.",
            "🟢 You may rely on it.",

            "🟢 As I see it, yes.",
            "🟢 Most likely.",
            "🟢 Outlook good.",
            "🟢 Yes.",
            "🟢 Signs point to yes.",

            "🟡 Reply hazy, try again.",
            "🟡 Ask again later.",
            "🟡 Better not tell you now.",
            "🟡 Cannot predict now.",
            "🟡 Concentrate and ask again.",

            "🔴 Don't count on it.",
            "🔴 My reply is no.",
            "🔴 My sources say no.",
            "🔴 Outlook not so good.",
            "🔴 Very doubtful."
        ]

        response = choice(choices)
        color = 0
        if response.startswith("🟢"): color = 0x00FF00
        if response.startswith("🟡"): color = 0xFFFF00
        if response.startswith("🔴"): color = 0xFF0000

        embed = Embed(
            title="8ball",
            description=f"*Question*: {question}\n*Response*: {response[1:]}",
            timestamp=datetime.now(tz=timezone.utc),
            color=Color(color)
        )

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(EightBall(bot))
