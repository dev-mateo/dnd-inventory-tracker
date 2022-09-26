from discord import Intents
from discord.ext.commands import Bot

import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("token")

class BotClass(Bot):
    def __init__(self):
        super().__init__(
            command_prefix=";",
            intents=Intents.all(),
        )

    async def load_extensions(self):

        for filename in os.listdir("cogs"):
            if filename.endswith(".py"):
                await bot.load_extension(f"cogs.{filename[:-3]}")
                # print(">>> Imported: "+filename)

        print(">>> Successfully imported modules")

    async def on_ready(self):
        await self.load_extensions()
        print(f">>> Logged in as: {self.user}")


if __name__ == "__main__":
    bot = BotClass()
    bot.run(TOKEN)