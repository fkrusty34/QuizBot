import sqlite3
from telebot.types import LabeledPrice

from loader import bot, provider_token, db_path, channel
from utils import costs
from utils import algs


@bot.message_handler(content_types=["web_app_data"])
def web_app(message):
    args = list(message.web_app_data.data.split("|"))

    # количество каждого блюда пользователя
    data = {}
    for i in range(len(costs.dishes)):
        data[costs.dishes[i]] = int(args[i])

    # массив с ценами на блюда пользователя для отправки счета
    prices = []
    for key in data:
        prices.append(data[key] > 0 and LabeledPrice(f"{key} x{data[key]}", data[key] * costs.costs[key]))

    # вычисляем стоимость заказа без чаевых
    total = 0
    for key in data:
        total += data[key] * costs.costs[key]

    # стоимость заказа должна быть выше цены 1$
    if total < 6400:
        bot.send_message(message.chat.id, "Минимальная сумма заказа - 64 руб.")
        return

    con = sqlite3.connect(db_path + "offer.db")
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS orders (
        id INT,
        user_id INT,
        ord TEXT,
        comment TEXT,
        sum INT
    )""")
    con.commit()

    cur.execute("SELECT id FROM orders ORDER BY id DESC")
    res = cur.fetchone()

    # вычисляем номер (id) заказа
    try:
        order_id = res[0] + 1
    except TypeError:
        order_id = 1

    # добавляем заказ в список всех заказов
    cur.execute("INSERT INTO orders VALUES (?, ?, ?, ?, ?)",
                (order_id, message.chat.id, " ".join(args[:-1]), args[-1], total))
    con.commit()

    con.close()

    # отправляем счет
    bot.send_invoice(
        chat_id=message.chat.id,
        title=f"Заказ #{res[0] + 1}",
        description="Тестовый заказ :)",
        invoice_payload=f"{res[0] + 1}",
        provider_token=provider_token,
        currency="RUB",
        prices=prices,

        max_tip_amount=10000,
        suggested_tip_amounts=[100, 200, 500],
        need_name=True,

        start_parameter=f"{res[0] + 1}"
    )


@bot.pre_checkout_query_handler(func=lambda query: True)
def pre_checkout_query(query):
    con = sqlite3.connect(db_path + "offer.db")
    cur = con.cursor()

    # получаем заказ
    order_id = int(query.invoice_payload)
    cur.execute("SELECT ord FROM orders WHERE id = ?", (order_id,))
    res = cur.fetchone()

    order = list(map(int, res[0].split()))

    # cur.execute("""CREATE TABLE IF NOT EXISTS remains (
    #     dish_1 INT,
    #     dish_2 INT,
    #     dish_3 INT
    # )""")

    cur.execute("PRAGMA table_info(remains)")
    res = cur.fetchall()

    cols = []
    for i in res:
        cols.append(i[1])

    cur.execute("SELECT * FROM remains")
    res = cur.fetchone()

    # проверяем, имеется ли товар
    for i in range(len(order)):
        if order[i] <= res[i]:
            continue
        else:
            bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=False,
                                          error_message="Выбранный вами товар отсутствует")
            break
    else:
        for i in range(len(order)):
            cur.execute(f"UPDATE remains SET {cols[i]} = ?", (res[i] - order[i],))
            con.commit()

        bot.answer_pre_checkout_query(pre_checkout_query_id=query.id, ok=True)

    con.close()


@bot.message_handler(content_types=["successful_payment"])
def invoice(message):
    # уведомляем пользователя о том что оплата прошла успешно и заказ начинает готовиться
    bot.send_message(message.chat.id, "Принято. Ваш заказ готовится")

    con = sqlite3.connect(db_path + "offer.db")
    cur = con.cursor()

    cur.execute("""CREATE TABLE IF NOT EXISTS payed_orders (
        id INT,
        user_id INT,
        user_name TEXT,
        ord TEXT,
        comment TEXT,
        amount INT,
        tips INT,
        cooker INT
    )""")
    con.commit()

    order_id = int(message.successful_payment.invoice_payload)

    cur.execute("SELECT * FROM orders WHERE id = ?", (order_id,))
    res = cur.fetchone()

    name = message.successful_payment.order_info.name
    total_amount = message.successful_payment.total_amount
    tips = total_amount - res[4]

    # формируем оплаченный заказ пользователя
    order = []
    for i in range(len(costs.dishes)):
        order.append(f"{costs.dishes[i]}: {res[2].split()[i]}" if int(res[2].split()[i]) > 0 else "")

    for _ in range(len(order)):
        try:
            order.remove("")
        except ValueError:
            break

    # добавляем оплаченный заказ в базу
    cur.execute("INSERT INTO payed_orders VALUES (?, ?, ?, ?, ?, ?, ?, 0)",
                (res[0], res[1], name, "&".join(order), res[3], res[4], tips))
    con.commit()

    con.close()

    # отправляем сообщение cook-ерам
    order_txt = "\n".join(order)
    comment = f"\n<b>Комментарий:</b>\n{res[3]}\n" if algs.trim(res[3]) != "" else "\n"

    bot.send_message(channel, f"#{res[0]}\n"
                              f"<b>Имя:</b> {name}\n"
                              f"<b>Заказ:</b>\n"
                              f"{order_txt}"
                              f"{comment}\n"
                              f"/cook\n"
                              f"/ready", parse_mode="HTML")
