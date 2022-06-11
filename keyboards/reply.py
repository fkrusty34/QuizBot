from telebot.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from telebot.types import WebAppInfo


def offer() -> ReplyKeyboardMarkup:
    """
    Заказать еду
    :return: ReplyKeyboardMarkup
    """
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    web_app = WebAppInfo("https://fkrusty34.github.io/quizBot_webApp/")
    markup.add(KeyboardButton("Заказать", web_app=web_app))
    return markup
