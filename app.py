import toml
import os

from hammerbot import bot
from hammerbot.utils import log, helpers

if __name__ == "__main__":

    config = helpers.load_config()

    bot = bot.HammerBot(config=config)

    bot.run(
        token=config.discord_api_key,
        log_handler=log.setup_logging(
            level=config.logging.level, formatter=config.logging.formatter
        ).handlers[0],
        log_formatter=log.generate_formatter(formatter=config.logging.formatter),
        log_level=config.logging.level,
        root_logger=True,
    )
