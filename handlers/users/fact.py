import sqlite3

from loader import bot, db_path
from keyboards import inline


@bot.callback_query_handler(func=lambda call: call.data == "fact")
def fact(call):
    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    cur.execute("SELECT last_fact FROM users WHERE id = ?", (call.message.chat.id,))
    res = cur.fetchone()

    if res[0] == 2:
        cur.execute("UPDATE users SET last_fact = 0 WHERE id = ?", (call.message.chat.id,))
    else:
        cur.execute("UPDATE users SET last_fact = ? WHERE id = ?", (res[0] + 1, call.message.chat.id))
    con.commit()

    con.close()

    con = sqlite3.connect(db_path + "facts.db")
    cur = con.cursor()

    cur.execute("SELECT fact FROM facts WHERE id = ?", (res[0],))
    res = cur.fetchone()

    bot.answer_callback_query(call.id)
    bot.edit_message_text(f"{res[0]}", chat_id=call.message.chat.id,
                          message_id=call.message.id, reply_markup=inline.fact())

    con.close()
