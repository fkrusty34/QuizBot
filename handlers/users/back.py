# from loader import bot
# from keyboards import inline
#
#
# @bot.callback_query_handler(func=lambda call: "back" in call.data)
# def back(call):
#     if call.data == "back.menu":
#         bot.answer_callback_query(call.id)
#         bot.edit_message_text("Также вам доступно:",
#                               chat_id=call.message.chat.id, message_id=call.message.id,
#                               reply_markup=inline.short_menu())
