from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


def full_menu(quiz_available: bool) -> InlineKeyboardMarkup:
    """
    Развернутое меню
    :param quiz_available: доступна ли викторина
    :return: клавиатура
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Факт о масленице", callback_data="fact"))
    if quiz_available:
        markup.add(InlineKeyboardButton("Викторина", callback_data="quiz"))
    markup.add(InlineKeyboardButton("↑ Свернуть", callback_data="show_less"))
    return markup


# def yn(yes="yes", no="no"):
#     markup = InlineKeyboardMarkup()
#     markup.add(InlineKeyboardButton("Да", callback_data=yes))
#     markup.add(InlineKeyboardButton("Нет", callback_data=no))
#     return markup


def confirm_quiz_start() -> InlineKeyboardMarkup:
    """
    Подтверждение начала "Викторины"
    :return: клавиатура
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Да", callback_data="quiz.yes"))
    markup.add(InlineKeyboardButton("← Назад", callback_data=f"back.menu"))
    return markup


def quiz(cur_num: int, r_ans: str) -> InlineKeyboardMarkup:
    """
    Клавиатура режима "Викторина"
    :param cur_num: номер текущего вопроса
    :param r_ans: правильный ответ
    :return: клавиатура
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("A", callback_data=f"quiz.next.{1 if r_ans == 'A' else 0}."
                                                       f"{'0' if cur_num + 1 < 10 else ''}{cur_num + 1}"),
               InlineKeyboardButton("C", callback_data=f"quiz.next.{1 if r_ans == 'C' else 0}."
                                                       f"{'0' if cur_num + 1 < 10 else ''}{cur_num + 1}"))
    markup.add(InlineKeyboardButton("B", callback_data=f"quiz.next.{1 if r_ans == 'B' else 0}."
                                                       f"{'0' if cur_num + 1 < 10 else ''}{cur_num + 1}"),
               InlineKeyboardButton("D", callback_data=f"quiz.next.{1 if r_ans == 'D' else 0}."
                                                       f"{'0' if cur_num + 1 < 10 else ''}{cur_num + 1}"))
    return markup


def short_menu() -> InlineKeyboardMarkup:
    """
    Свернутое меню
    :return: клавиатура
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("↓ Развернуть", callback_data="show_more"))
    return markup


def back_to_menu() -> InlineKeyboardMarkup:
    """
    Клавиатура с кнопкой "назад"
    :param to: callback-дата кнопки "Назад"
    :return:
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("← Назад", callback_data=f"back.{to}"))
    return markup


def fact() -> InlineKeyboardMarkup:
    """
    Клавиатура режима "Факт"
    :return: клавиатура
    """
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("Следующий факт", callback_data="fact"))
    markup.add(InlineKeyboardButton("← Назад", callback_data="back.menu"))
    return markup
