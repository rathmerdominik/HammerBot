import sys
import logging

import os
from os import listdir
from os import path

from discord import Intents
from discord.ext import commands

from hammerbot.types.config import Config

logger = logging.getLogger(__name__)

@commands.command()
@commands.is_owner()
async def close_bot(ctx: commands.context.Context):
    await ctx.send("Shutting down bot! Have a good day", ephemeral=True)
    logger.info("Bot shutdown")
    await ctx.bot.close()


def restart_program():
    python = sys.executable
    os.execl(python, python, *sys.argv)


@commands.command()
@commands.is_owner()
async def restart_bot(ctx: commands.context.Context):
    logger.info("Bot restarting")
    await ctx.send("Bot is restarting now!", ephemeral=True)
    
    restart_program()


class HammerBot(commands.Bot):
    def __init__(self, config: Config):
        
        intents = Intents.default()
        intents.message_content = True
        intents.members = True

        super().__init__("!", intents=intents, owner_ids=config.bot_owner_ids)

    async def setup_hook(self) -> None:
        
        self.add_command(close_bot)
        logger.debug("Add commands close_bot")
        self.add_command(restart_bot)
        logger.debug("Added command restart bot")
        
        await self.load_all_modules()
        
        self.available_cogs = self.cogs.copy()
        self.available_extensions = self.extensions.copy()
        


    async def load_all_modules(self):
        extension_dir = path.dirname(__file__) + "/modules"
        
        for file in listdir(extension_dir):
            logger.debug(file)
            if file.endswith(".py"):
                logger.debug(file)
                await self.load_extension(f"hammerbot.modules.{file[:-3]}")
                
        logger.info("All modules loaded")

    
    async def on_command_error(
        self,
        ctx: commands.context.Context,
        exception: commands.errors.CommandError,
    ) -> None:
        try:
            raise exception
        
        except commands.errors.NotOwner:
            logger.exception(
                f"{ctx.author} tried executing {ctx.command} with insufficent permissions"
            )
            await ctx.send(
                "You do not have permission to execute this command", ephemeral=True
            )
            
        except commands.errors.CommandNotFound as e:
            logger.exception(f"{e}. Asked by {ctx.author}")
            await ctx.send(f"Command \"{ctx.message.content}\" not found")
            
        except Exception as e:
            logger.exception(f"Error not handled: {e}")
            if ctx.author.id in self.owner_ids:
                await ctx.send(f"```py\n {e} ```", ephemeral=True)
            else:
                await ctx.send("Encountered an Error that is not handled. Please contact an Admin", ephemeral=True)
            
