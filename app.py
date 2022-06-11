import logging
from utils.notify_admins import on_startup_notify
from loader import bot

import handlers


def run_logging():
    fmt = "%(asctime)s (%(funcName)s:%(lineno)d) %(levelname)s - %(message)s"
    logging.basicConfig(filename="logs.log", level=logging.INFO, format=fmt)


if __name__ == "__main__":
    run_logging()
    logging.info("Bot is running")
    on_startup_notify()

    bot.infinity_polling()
