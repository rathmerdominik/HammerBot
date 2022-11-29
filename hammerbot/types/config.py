from typing import List
from pydantic import BaseModel


class Logging(BaseModel):
    formatter: str
    level: str


class Config(BaseModel):
    discord_api_key: str
    bot_owner_ids: List[int]
    logging: Logging
