import sqlite3
from random import shuffle
from time import sleep

from loader import bot, db_path
from keyboards import inline


@bot.callback_query_handler(func=lambda call: call.data == "quiz")
def quiz_sure(call):
    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    cur.execute("SELECT quiz_status FROM users WHERE id = ?", (call.message.chat.id,))
    res = cur.fetchone()

    if res[0] == -1:
        bot.edit_message_text("Вы уверены? Викторину можно пройти только 1 раз и нельзя остановить",
                              chat_id=call.message.chat.id, message_id=call.message.id,
                              reply_markup=inline.confirm_quiz_start())
    else:
        bot.answer_callback_query(call.id, "Вы уже проходите или прошли викторину", show_alert=True)

    con.close()


@bot.callback_query_handler(func=lambda call: call.data == "quiz.yes")
def quiz_chk(call):
    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    cur.execute("SELECT quiz_status FROM users WHERE id = ?", (call.message.chat.id,))
    res = cur.fetchone()

    if res[0] == -1:
        cur.execute("UPDATE users SET quiz_status = 0 WHERE id = ?", (call.message.chat.id,))
        con.commit()
        bot.answer_callback_query(call.id)
        call.data = "quiz.next.0.00"
        quiz(call)
    else:
        bot.answer_callback_query(call.id, "Вы уже проходите или прошли викторину", show_alert=True)

    con.close()


@bot.callback_query_handler(func=lambda call: call.data[:-4] == "quiz.next.")
def quiz(call):
    args = call.data.split(".")[2:]

    # con = sqlite3.connect("./db/quiz.db")
    # cur = con.cursor()
    #
    # cur.execute("SELECT cur_num FROM quiz")
    # res = cur.fetchall()
    #
    # con.close()

    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    cur.execute("UPDATE users SET tmp = ? WHERE id = ?", (args[-1], call.message.chat.id))
    con.commit()

    con.close()

    if args[0] == "1":
        con = sqlite3.connect(db_path + "users.db")
        cur = con.cursor()
        cur.execute("SELECT quiz_status FROM users WHERE id = ?", (call.message.chat.id,))
        res = cur.fetchone()

        cur.execute("UPDATE users SET quiz_status = ? WHERE id = ?", (res[0] + 1, call.message.chat.id))
        con.commit()

        con.close()

    if args[1] == "10":
        con = sqlite3.connect(db_path + "users.db")
        cur = con.cursor()

        cur.execute("UPDATE users SET tmp = ? WHERE id = ?", ("0", call.message.chat.id))
        con.commit()

        cur.execute("SELECT quiz_status FROM users WHERE id = ?", (call.message.chat.id,))
        bot.edit_message_text(f"Викторина пройдена. Вы получаете скидку {cur.fetchone()[0]}% на заказ от 25 руб.",
                              chat_id=call.message.chat.id, message_id=call.message.id,
                              reply_markup=inline.back_to_menu())

        bot.answer_callback_query(call.id)

        con.close()
        return

    con = sqlite3.connect(db_path + "quiz.db")
    cur = con.cursor()

    cur.execute("SELECT que, answer, answers FROM quiz WHERE num = ?", (args[1],))
    res = cur.fetchone()

    que = res[0]
    ans = [res[1]] + list(res[2].split("*"))
    shuffle(ans)

    num = int(args[1])
    r = chr(ans.index(res[1]) + 65)
    markup = inline.quiz(cur_num=num, r_ans=r)

    # noinspection PyBroadException
    try:
        bot.answer_callback_query(call.id)
    except Exception:
        pass

    text = f"<b>Вопрос №{num + 1}</b>" \
           f"\n{que}" \
           f"\n<b>A)</b> {ans[0]}" \
           f"\n<b>B)</b> {ans[1]}" \
           f"\n<b>C)</b> {ans[2]}" \
           f"\n<b>D)</b> {ans[3]}"

    con.close()

    con = sqlite3.connect(db_path + "users.db")
    cur = con.cursor()

    for i in range(10, 0, -1):
        cur.execute("SELECT tmp FROM users WHERE id = ?", (call.message.chat.id,))
        res = cur.fetchone()
        if int(res[0]) != num:
            con.close()
            return
        bot.edit_message_text(text + f"\nОсталось {i} "
                                     f"{'секунда' if i % 10 in [1] else 'секунды' if i % 10 in [2, 3, 4] else 'секунд'}"
                              , chat_id=call.message.chat.id, message_id=call.message.id,
                              parse_mode="HTML", reply_markup=markup)
        sleep(1)

    cur.execute("SELECT tmp FROM users WHERE id = ?", (call.message.chat.id,))
    res = cur.fetchone()

    con.close()

    if int(res[0]) != num:
        return

    call.data = f"quiz.next.0.{0 if num + 1 < 10 else ''}{num + 1}"

    quiz(call)
