import logging

from . import helpers


def setup_logging_from_config() -> logging.Logger:
    """Generates a logger based on HammerBots toml config

    Returns:
        logging.Logger: The finished logger
    """
    config = helpers.load_config()
    return setup_logging(level=config.logging.level, formatter=config.logging.formatter)


def setup_logging(
    name: str = __name__, level: str = "WARNING", formatter: logging.Formatter = None
) -> logging.Logger:
    """Create a logger with given name, log level and formatter

    Args:
        name (str, optional): The namespace for the logger. Defaults to __name__.
        level (str, optional): The log level to set the logger to. Defaults to "WARNING".
        formatter (logging.Formatter, optional): Formatting for the logger. Defaults to None.

    Returns:
        logging.Logger: The logger object
    """
    logger = logging.getLogger(name)

    formatter = generate_formatter(formatter)

    handler = logging.StreamHandler()

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    level = logging.getLevelName(level)
    logger.setLevel(level)

    return logger


def generate_formatter(formatter: str = None) -> logging.Formatter:
    """Helper function to generate a formatter based on a standard string or on a given string

    Args:
        formatter (str): the string to use for formatting. Defaults to None

    Returns:
        logging.Formatter: The finished formatter
    """
    if not formatter:
        formatter = logging.Formatter(
            fmt="%(asctime)s - %(levelname)s - %(module)s - %(message)s"
        )
    else:
        formatter = logging.Formatter(fmt=formatter)

    return formatter
