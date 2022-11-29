from typing import Optional, Dict
from pydantic import BaseModel


class Channel(BaseModel):
    emoji_assign: Optional[int]
    description: Optional[str]
    channels: Optional[Dict[str, str]]


class ChannelLayout(BaseModel):
    channel_for_welcome: int
    guild_to_manage: int
    message_id_for_welcome: int
    enable_server_nuke: bool

    categories: Dict[str, Channel]
