from pydantic import BaseModel


class Module(BaseModel):
    name: str
    enabled: bool
