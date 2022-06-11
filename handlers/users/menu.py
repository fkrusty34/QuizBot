import sqlite3

from loader import bot, db_path
from keyboards import inline


@bot.callback_query_handler(func=lambda call: call.data == "show_more")
def full_menu(call, start=False):
    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    cur.execute("SELECT quiz_status FROM users WHERE id = ?", (call.message.chat.id,))
    res = cur.fetchone()

    markup = inline.full_menu(True if res[0] == -1 else False)

    bot.answer_callback_query(call.id)

    if start:
        bot.edit_message_text("Вам доступно:", chat_id=call.message.chat.id,
                              message_id=call.message.id, reply_markup=markup)
    else:
        bot.edit_message_text(call.message.text, chat_id=call.message.chat.id,
                              message_id=call.message.id, reply_markup=markup)

    con.close()


@bot.callback_query_handler(func=lambda call: call.data == "show_less")
def short_menu(call):
    markup = inline.short_menu()

    bot.answer_callback_query(call.id)
    bot.edit_message_text(call.message.text, chat_id=call.message.chat.id,
                          message_id=call.message.id, reply_markup=markup)


@bot.callback_query_handler(func=lambda call: call.data == "back.menu")
def back(call):
    full_menu(call, start=True)
