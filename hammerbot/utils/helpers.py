import os
import toml

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


def write_config(config: Config) -> None:
    """Saves HammerBots config in its toml file

    Args:
        config (Config): config object
    """
    root = os.path.join(os.path.dirname(__file__), "../..")

    with open(f"{root}/config.toml", "w") as f:
        config = config.dict()
        toml.dump(config, f)
