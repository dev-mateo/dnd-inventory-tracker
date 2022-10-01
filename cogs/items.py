import discord
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

class Paginator(discord.ui.View):
    def __init__(self, user, pages):
        super().__init__(timeout=300.0)
        self.user = user
        self.pages = pages
        self.current_page = 0
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        if len(self.pages) == 1:
            self.rightButton.disabled=True

    @discord.ui.button(emoji='⏪', style=discord.ButtonStyle.blurple, disabled=True)
    async def leftMax(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            await interaction.response.send_message(f"You're not {self.user.mention}... are you?", ephemeral=True)
            return False
        
        self.rightButton.disabled = False
        self.rightMax.disabled = False
        
        self.leftButton.disabled = True
        self.leftMax.disabled = True

        self.current_page = 1

        self.indexButton.label = f"1/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[1], view=self)   

    @discord.ui.button(emoji='⬅️', style=discord.ButtonStyle.blurple, disabled=True)
    async def leftButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            await interaction.response.send_message(f"You're not {self.user.mention}... are you?", ephemeral=True)
            return False
        if self.current_page - 1 == 0:
            self.leftButton.disabled = True
            self.leftMax.disabled = True
            
        self.rightButton.disabled = False
        self.rightMax.disabled = False
        
        self.current_page -= 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)

    @discord.ui.button(label=f'1', style=discord.ButtonStyle.gray, disabled=True)
    async def indexButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        pass

    @discord.ui.button(emoji='➡️', style=discord.ButtonStyle.blurple)
    async def rightButton(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            await interaction.response.send_message(f"You're not {self.user.mention}... are you?", ephemeral=True)
            return False
        if self.current_page + 1 == len(self.pages) - 1:
            self.rightButton.disabled = True
            self.rightMax.disabled = True

        self.leftButton.disabled = False
        self.leftMax.disabled = False

        self.current_page += 1
        self.indexButton.label = f"{self.current_page + 1}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[self.current_page], view=self)


    @discord.ui.button(emoji='⏩', style=discord.ButtonStyle.blurple)
    async def rightMax(self, interaction: discord.Interaction, button: discord.ui.Button):
        if self.user.id != interaction.user.id:
            await interaction.response.send_message(f"You're not {self.user.mention}... are you?", ephemeral=True)
            return False
        
        self.rightButton.disabled = True
        self.rightMax.disabled = True

        self.leftButton.disabled = False
        self.leftMax.disabled = False

        self.current_page = len(self.pages)

        self.indexButton.label = f"{len(self.pages)}/{len(self.pages)}"
        await interaction.response.edit_message(embed=self.pages[-1], view=self)   


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
        
        embeds = [embed]

        for x in _object:
            for y in x:
                
                if y.upper() == "USER" or y.upper() == "_ID":
                    continue

                items = str(x[y]).replace("'", "").replace("[", "• ").replace("]", "").replace(",", "\n• ")

                new_page = Embed(
                    title=y.upper(),
                    description=items
                )

                embeds.append(new_page)
        
        await interaction.response.send_message(embed=embed, view=Paginator(interaction.user, embeds))


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Items(bot))
