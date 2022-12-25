import os
import re
import toml


from ..types.config import Config


def camel_to_snake(text: str) -> str:
    """Converts camel to snake case

    Args:
        text (str): text to convert

    Returns:
        str: the converted text
    """
    return re.sub(r"(?<!^)(?=[A-Z])", "_", text).lower()


def load_config() -> Config:
    """Loads core config from its toml file

    Returns:
        Config: The config object
    """
    module_root = os.path.join(os.path.dirname(__file__), "..")

    with open(f"{module_root}/core.toml") as f:
        config: dict = toml.load(f)
        config: Config = Config(**config)

    return config
