import re
import os
import toml

from uuid import uuid4, UUID

from typing import List

from ..types.config import Config


def load_config() -> Config:
    """Loads HammerBots config from its toml file

    Returns:
        Config: The config object
    """
    root = os.path.join(os.path.dirname(__file__), "../..")

    with open(f"{root}/config.toml") as f:
        config: dict = toml.load(f)
        config: Config = Config(**config)

    return config


def camel_to_snake(text: str) -> str:
    """Converts camel to snake case

    Args:
        text (str): text to convert

    Returns:
        str: the converted text
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()
