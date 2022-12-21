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


def generate_uuid_from_int_list(int_list: List[int]) -> UUID:

    hex_list = []

    for i in int_list:
        if i < 0:
            i = i + 2**32
        print(hex(i)[2:])
        hex_list.append(hex(i)[2:])

    return UUID("".join(hex_list))


print(generate_uuid_from_int_list([-40106919, 1701661571, -1858771250, -1113751207]))
