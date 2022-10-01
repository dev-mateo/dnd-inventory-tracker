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

class Update(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.col = get_database(CONNECT)

    @app_commands.command(
        name="update",
        description="Update a player's item"
    )
    @app_commands.describe(
        user="The user you want to update an item",
        category="The item's category",
        item="The item you want to update",
        new_value="The value to update"
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
    async def update(self, interaction: Interaction, user: Member, category: Choice[str], item: str, new_value: str) -> None:
        
        query = {"user": str(user.id)}

        val1 = {"$pull": { category.value: item }}
        self.col.update_one(query, val1)

        val2 = {"$push": { category.value: new_value }}
        self.col.update_one(query, val2)

        embed = Embed(
            title="Update",
            description=f"> {user.mention}'s `{item}` has been updated to `{new_value}` "
        )
        embed.set_footer(text=interaction.user, icon_url=interaction.user.avatar)

        await interaction.response.send_message(embed=embed)
        return


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Update(bot))
