from loader import bot, admins


def on_startup_notify():
    for admin in admins:
        try:
            bot.send_message(admin, "Bot is running")
        except Exception:
            pass


def on_disturb_notify():
    for admin in admins:
        try:
            bot.send_message(admin, "Bot is stopped")
        except Exception:
            pass
