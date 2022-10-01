from discord import app_commands, Interaction, Member, Embed
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

class Items(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        self.col = get_database(CONNECT)

    @app_commands.command(
        name="items",
        description="Get the inventory of a dnd player"
    )
    @app_commands.checks.has_role(806958702400634920)
    @app_commands.checks.cooldown(1, 5.0, key=lambda i: (i.guild_id, i.user.id))
    async def items(self, interaction: Interaction, user: Member) -> None:
        _object = self.col.find({"user":str(user.id)})
        embed = Embed(
            title="Inventory",
            description=f"{user.mention}'s inventory"
        )
        
        for x in _object:
            for y in x:
                
                if y.upper() == "USER" or y.upper() == "_ID":
                    continue

                items = str(x[y]).replace("'", "").replace("[", "• ").replace("]", "").replace(",", "\n• ")

                embed.add_field(
                    name=y.upper(),
                    value=items
                )
        
        await interaction.response.send_message(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Items(bot))
