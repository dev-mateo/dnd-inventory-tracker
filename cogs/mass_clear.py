from discord import app_commands, Interaction, Member, Embed
from discord.app_commands import Choice
from discord.ext import commands
from os import getenv
from dotenv import load_dotenv # Get the bot's token
from pymongo import MongoClient

load_dotenv() 
CONNECT = getenv("connect") 

def get_database(c):
   client = MongoClient(c)
   db = client.get_database("DND_DB")
   return db.get_collection('DND_COL')

class Clear(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.col = get_database(CONNECT)

    @app_commands.command(
        name="clear",
        description="Mass clear a category"
    )
    @app_commands.describe(
        user="The user whose category you want to mass clear",
        category="The category to mass clear",
    )
    @app_commands.choices(
        category=[
                Choice(name="Party Resources", value="party_resources"),
                Choice(name="Assets", value="assets"),
                Choice(name="Items", value="items"),
                Choice(name="Miscellaneous ", value="misc"),
                Choice(name="Boat Supplies", value="boat_supplies")
            ]
    )
    @app_commands.checks.has_permissions(administrator=True)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def clear(self, interaction: Interaction, user: Member, category: Choice[str]) -> None:
        
        query = {"user": str(user.id)}
        new_value = {"$set": { category.value: [] }}
        self.col.update_one(query, new_value)

        embed = Embed(
            title="Category Clear",
            description=f"> `{category.name}` has been cleared from {user.mention}"
        )
        embed.set_footer(text=interaction.user, icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Clear(bot))
