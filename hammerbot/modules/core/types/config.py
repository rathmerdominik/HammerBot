from pydantic import BaseModel


class Config(BaseModel):
    database_path: str
