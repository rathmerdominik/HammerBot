import toml
import logging
import discord

from typing import List

from pathlib import Path

from discord.ext import commands
from discord.ext.commands import Bot, Cog

from discord.guild import Guild
from discord.channel import CategoryChannel

from hammerbot.types.channel_layout import ChannelLayout


logger = logging.getLogger(__name__)


class ChannelManager(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.config = self.load_config()
        if not self.config.guild_to_manage:
            logger.warning("No guild has been set to manage. Disabling ChannelManager")
            self.bot.unload_extension(self.__module__)

        logger.debug(self.config)

    def load_config(self) -> ChannelLayout:
        """Returns a type from the channel_manager config file

        Returns:
            ChannelLayout: The model from the config file
        """
        project_path = Path(__file__).parents[2]
        with open(f"{project_path}/channel_manager.toml") as f:
            return ChannelLayout(**toml.load(f))

    def save_config(self):
        project_path = Path(__file__).parents[2]
        with open(f"{project_path}/channel_manager.toml", "w") as f:
            toml.dump(self.config.dict(), f)

    @commands.hybrid_command()
    @commands.is_owner()
    async def clear_all_channels(
        self, ctx: commands.context.Context, confirm: str = ""
    ):
        """Clears all channels and categories"""

        if not self.config.enable_server_nuke:
            await ctx.send(
                "Clearing of every channel has been disabled in the config. Please set `enable_server_nuke` to `true` to enable it!",
                ephemeral=True,
            )
            logger.warn("Server nuking invoked with nuking disabled in config file")
            return

        if confirm != "Yes. Do as i say":
            await ctx.send(
                'Please pass the parameter "Yes. Do as i say" to confirm your intention to **delete all** channels',
                ephemeral=True,
            )
            logger.warn("Server nuking invoked without intention confirmation")
            return

        logger.warn("Server nuking initialized! Destroying all channels and categories")

        await ctx.send("Starting server nuking!", ephemeral=True)

        for category in ctx.guild.categories:
            logger.info(f"{category} Category deleted")
            await category.delete()

        for channel in ctx.guild.channels:
            try:
                await channel.delete()
                logger.info(f"{channel} Channel deleted")
            except discord.HTTPException as e:
                logger.warn(f"Cannot delete channel {channel.name}. Reason: {e.text}")
                continue

    @commands.hybrid_command()
    @commands.is_owner()
    async def clear_all_roles(self, ctx: commands.context.Context, confirm: str = ""):
        """Clears all roles"""

        if not self.config.enable_server_nuke:
            await ctx.send(
                "Clearing of every role has been disabled in the config. Please set `enable_server_nuke` to `true` to enable it!",
                ephemeral=True,
            )
            logger.warn("Role nuking invoked with nuking disabled in config file")
            return

        if confirm != "Yes. Do as i say":
            await ctx.send(
                'Please pass the parameter "Yes. Do as i say" to confirm your intention to **delete all** roles',
                ephemeral=True,
            )
            logger.warn("Role nuking invoked without intention confirmation")
            return

        logger.warn("Role nuking initialized! Destroying all roles!")

        await ctx.send("Starting role nuking!", ephemeral=True)

        for role in ctx.guild.roles:
            try:
                await role.delete()
                logger.info(f"{role.name} Role deleted")
            except discord.HTTPException as e:
                logger.warn(f"Cannot delete role {role.name}. Reason: {e.text}")
                continue

    async def build_welcome_message(self, guild: Guild) -> discord.Embed:
        """Builds  a welcome message based on category, emojis ahd description

        Args:
            guild (Guild): Managed guild

        Returns:
            discord.Embed: created Embed
        """
        embed = discord.Embed(
            colour=0x00FF00,
            title="Role assignment",
            description="Assignment of roles based on reaction",
        )
        for category in self.config.categories:
            emoji = self.bot.get_emoji(self.config.categories[category].emoji_assign)
            description = self.config.categories[category].description

            embed.add_field(
                name=f"{category} | {emoji}", value=description, inline=False
            )

        return embed

    async def assign_emojis(self, guild: Guild):

        channel = guild.get_channel(self.config.channel_for_welcome)

        message: discord.Message = await channel.fetch_message(
            self.config.message_id_for_welcome
        )

        await message.clear_reactions()

        for category in self.config.categories:

            emoji = self.bot.get_emoji(self.config.categories[category].emoji_assign)

            try:
                await message.add_reaction(emoji)
            except TypeError as e:
                logger.warn(
                    f"Emoji not found with id: {self.config.categories[category].emoji_assign}"
                )

    async def create_channels(self, guild: Guild):
        category_channels: List[CategoryChannel] = guild.categories

        for category in self.config.categories:
            if not discord.utils.get(category_channels, name=category):
                created_category = await guild.create_category(category)
                if not discord.utils.get(guild.roles, name=category):

                    role = await guild.create_role(
                        name=category, mentionable=True, hoist=True
                    )
                    logger.debug(role)

                    await created_category.set_permissions(
                        guild.default_role, view_channel=False
                    )
                    await created_category.set_permissions(role, view_channel=True)

                    logger.info(f"Created category: {created_category.name}")

                category_channels.append(created_category)

        for category in category_channels:
            if category.name not in self.config.categories:
                continue

            for channel in self.config.categories[category.name].channels:
                if not discord.utils.get(category.channels, name=channel):

                    match self.config.categories[category.name].channels[channel]:
                        case "text":
                            logger.info(
                                f"Creating text channel {channel} in {category}"
                            )
                            created_channel = await category.create_text_channel(
                                channel
                            )
                        case "voice":
                            logger.info(
                                f"Creating voice channel {channel} in {category}"
                            )
                            created_channel = await category.create_voice_channel(
                                channel
                            )
                        case "forum":
                            logger.info(
                                f"Creating forum channel {channel} in {category}"
                            )
                            created_channel = await category.create_forum(
                                channel, topic=channel
                            )
                        case "stage":
                            logger.info(
                                f"Creating stage channel {channel} in {category}"
                            )
                            created_channel = await category.create_stage_channel(
                                channel, topic=channel
                            )
                        case "announcement":
                            logger.info(
                                f"Creating announcement channel {channel} in {category}"
                            )
                            created_channel = await category.create_text_channel(
                                channel, news=True
                            )
                        case "nsfw":
                            logger.info(
                                f"Creating NFSW channel {channel} in {category}"
                            )
                            created_channel = await category.create_text_channel(
                                channel, nsfw=True
                            )
                        case _:
                            logger.warn(
                                f'"{channel}" has invalid channel type "{self.config.categories[category.name].channels[channel]}"'
                            )
                    try:
                        await created_channel.edit(sync_permissions=True)
                    except UnboundLocalError as e:
                        logger.debug(e)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        logger.debug(payload)
        if payload.member.id == self.bot.user.id:
            return

        for category in self.config.categories:

            current_category = self.config.categories[category]

            if (
                payload.emoji.id == current_category.emoji_assign
                and payload.message_id == self.config.message_id_for_welcome
            ):
                role: discord.Role = discord.utils.get(
                    payload.member.guild.roles, name=category
                )

                await payload.member.add_roles(role)
                logger.info(f"Assigned role {role.name} to {payload.member.name}")

                guild = self.bot.get_guild(payload.guild_id)
                emoji = self.bot.get_emoji(payload.emoji.id)
                channel = guild.get_channel(payload.channel_id)

                message: discord.Message = await channel.fetch_message(
                    payload.message_id
                )

                await message.remove_reaction(emoji, payload.member)

    @commands.Cog.listener()
    async def on_ready(self):

        bot: Bot = self.bot

        guild: Guild = bot.get_guild(self.config.guild_to_manage)

        await self.create_channels(guild)
        if self.config.message_id_for_welcome:
            try:
                channel = guild.get_channel(self.config.channel_for_welcome)

                message = await channel.fetch_message(
                    self.config.message_id_for_welcome
                )
                await message.edit(embed=await self.build_welcome_message(guild))

            except AttributeError as e:
                logger.error(
                    f"Channel ID seems to be corrupted! Please check if the ID is still correct."
                )
                return

            except discord.HTTPException as e:
                channel = guild.get_channel(self.config.channel_for_welcome)
                message: discord.message.Message = await channel.send(
                    embed=await self.build_welcome_message(guild)
                )

                self.config.message_id_for_welcome = message.id
                self.save_config()

        await self.assign_emojis(guild)
        logger.info(f'Starting to monitor "{guild.name}"')


async def setup(bot: Bot):
    logger.info("Channel Manager locked and loaded!")
    await bot.add_cog(ChannelManager(bot))
