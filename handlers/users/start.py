import sqlite3
from datetime import datetime

from loader import bot, db_path
from keyboards import inline, reply


@bot.message_handler(commands=["start"])
def start(message):
    if message.chat.type != "private":
        return

    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS users (
        id INT,
        reg_date TEXT,
        quiz_status INT,
        last_fact INT
    )""")
    con.commit()

    cur.execute("SELECT id FROM users WHERE id = ?", (message.chat.id,))
    res = cur.fetchone()

    if res is None:
        now = datetime.now()
        cur.execute("INSERT INTO users VALUES (?, ?, -1, 0, '0')", (message.chat.id, str(now)))
        con.commit()

        bot.send_message(message.chat.id, "Вас приветствует бот, созданный для "
                                          "интерактивного взаимодействия с магазином 7б класса")

        # bot.send_message(message.chat.id, "<i>Вы успешно зарегистрированы в системе</i>", parse_mode="HTML")

    bot.send_message(message.chat.id, "Чтобы заказать еду, нажмите на кнопку 'Заказать'",
                     reply_markup=reply.offer())
    bot.send_message(message.chat.id, "Вам доступно:", reply_markup=inline.short_menu())

    con.close()
