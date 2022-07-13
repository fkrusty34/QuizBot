from loader import bot, bot_ver


@bot.message_handler(commands=["help"])
def start(message):
    if message.chat.type != "private":
        return

    bot.send_message(message.chat.id, f"Версия бота {bot_ver}\n"
                                      f"<i>Скоро здесь будет список команд</i>", parse_mode="HTML")
