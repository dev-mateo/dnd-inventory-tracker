import discord
from typing import Optional, Literal
from discord.ext import commands
from discord.ext.commands import Greedy

class Sync(commands.Cog):

    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot


    @commands.command(
    name="sync",
    description="sync all slash commands"
    )
    @commands.guild_only()
    @commands.is_owner()
    async def sync(self, ctx, guilds: Greedy[discord.Object], spec: Optional[Literal["~", "*", "^"]] = None) -> None:
        if not guilds:
            if spec == "~":
                synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "*":
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == "^":
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()

            await ctx.send(
            f"Synced {len(synced)} commands {'globally' if spec is None else 'to the current guild.'}"
            )
            return

        ret = 0
        for guild in self.bot.guilds:
            try:
                await ctx.bot.tree.sync(guild=guild)
            except discord.HTTPException:
                pass
            else:
                ret += 1
        await ctx.send(f"Synced the tree to {ret}/{len(guilds)}.")

async def setup(bot):
    await bot.add_cog(Sync(bot))