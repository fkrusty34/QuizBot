import sqlite3

from loader import bot, db_path


@bot.message_handler(chat_types=["group"])
@bot.message_handler(commands=["cook"])
def cook(message):
    con = sqlite3.connect(db_path + "offer.db")
    cur = con.cursor()

    try:
        order_id = message.reply_to_message.text.split()[0][1:]
    except AttributeError:
        con.close()
        return

    cur.execute("SELECT cooker FROM payed_orders WHERE id = ?", (order_id,))
    res = cur.fetchone()

    if res[0] == 0:
        cur.execute("UPDATE payed_orders SET cooker = ? WHERE id = ?", (message.from_user.id, order_id))
        con.commit()
        bot.reply_to(message, "Принято")
    else:
        bot.reply_to(message, "Заказ уже выполнен или его выполняет другой человек")

    con.close()
