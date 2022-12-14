import logging

from discord import Embed
from discord.ext import commands
from discord.ext.commands import Cog, Bot

from .utils import db
from .utils.helpers import camel_to_snake


logger = logging.getLogger(__name__)


class Core(Cog):
    def __init__(self, bot: commands.Bot):
        self.bot: Bot = bot

    @commands.hybrid_command()
    @commands.is_owner()
    async def get_all_modules(self, ctx: commands.context.Context) -> None:

        loaded = "📥"
        unloaded = "📤"

        logger.debug(self.bot.available_cogs)
        logger.debug(self.bot.cogs)

        all_cogs = self.bot.available_cogs.keys()
        available_cogs = self.bot.cogs.keys()

        embed = Embed(title="Modules", description="Available Modules", color=0x00FFFF)
        for cog in all_cogs:
            if cog in available_cogs:
                embed.add_field(name=f"{cog}", value=f"{loaded}", inline=False)
            else:
                embed.add_field(name=f"{cog} ", value=f"{unloaded}", inline=False)

        await ctx.send(ephemeral=True, embed=embed)

    @commands.hybrid_command()
    @commands.is_owner()
    async def disable_module(self, ctx: commands.context.Context, module: str) -> None:

        if camel_to_snake(module) == "core":
            logger.warning(f"Disabled core module. Disabled by {ctx.author}")
            await ctx.send(
                "Disabling the core module leads to a loss of module control and is not recommended!\nYou will have to delete the database file or change 'enabled' to True for the Core module",
                ephemeral=True,
            )
        try:
            await self.bot.unload_extension(
                f"hammerbot.modules.{camel_to_snake(module)}.{camel_to_snake(module)}"
            )
            db.insert_module(camel_to_snake(module), enabled=False)

            logger.info(f"Disabled module {module}. Disabled by {ctx.author}")
            await ctx.send(f"Disabled Module: {module}", ephemeral=True)
        except commands.errors.ExtensionNotLoaded as e:
            logger.info(e)
            await ctx.send("Module not loaded or non-existent", ephemeral=True)

    @commands.hybrid_command()
    @commands.is_owner()
    async def enable_module(self, ctx: commands.context.Context, module: str) -> None:

        try:
            await self.bot.load_extension(
                f"hammerbot.modules.{camel_to_snake(module)}.{camel_to_snake(module)}"
            )
            db.insert_module(camel_to_snake(module), enabled=True)

        except commands.errors.ExtensionNotFound as e:
            logger.info(e)
            await ctx.send("Extension does not exist", ephemeral=True)
            return
        except commands.errors.ExtensionAlreadyLoaded as e:
            logger.info(e)
            await ctx.send("Extension is already loaded!", ephemeral=True)
            return
        except commands.errors.ExtensionFailed as e:
            logger.exception(e)
            await ctx.send(
                f"The extension could not be loaded: ```py\n{e}```", ephemeral=True
            )
            return

        await ctx.send(f"Enabled Module: {module}", ephemeral=True)

    @commands.hybrid_command()
    @commands.is_owner()
    async def reload_module(self, ctx: commands.context.Context, module: str) -> None:
        cog: Cog = self.bot.get_cog(module)
        if cog is None:
            await ctx.send(
                f"Cog not found. Please validate your input! You tried to reload: {module}",
                ephemeral=True,
            )
            return

        await self.bot.reload_extension(cog.__module__)
        await ctx.send(f"Reloaded Module: {module}", ephemeral=True)

    @commands.hybrid_command()
    @commands.is_owner()
    async def sync(self, ctx: commands.context.Context) -> None:
        fmt = await ctx.bot.tree.sync()

        logger.info(f"{ctx.author} synced command tree")
        await ctx.send(
            f"Command Tree synced! Found {len(fmt)} commands!", ephemeral=True
        )

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        try:
            for cog in list(self.bot.cogs.keys()):
                module = db.get_module(camel_to_snake(cog))

                logger.debug(module)
                if module == None:
                    db.insert_module(camel_to_snake(cog))
                    continue

                if not module.enabled:

                    await self.bot.unload_extension(
                        f"hammerbot.modules.{camel_to_snake(module.name)}.{camel_to_snake(module.name)}"
                    )
        except FileNotFoundError:
            logger.error(
                "core.toml does not exist! Please make sure that you created it out of the config.dist.toml file"
            )


async def setup(bot: commands.Bot):
    logger.info("Core Module locked and loaded!")
    await bot.add_cog(Core(bot))


async def teardown(bot: commands.Bot):
    logger.info("Core Module unloaded!")
