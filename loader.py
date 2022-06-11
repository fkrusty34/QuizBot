import logging
from telebot import TeleBot

from data import config


bot = TeleBot(config.BOT_TOKEN)
provider_token = config.PROVIDER_TOKEN
admins = config.ADMINS
channel = config.CHANNEL
db_path = "./utils/db/"
bot_ver = 1.0
