from telegram.ext import Filters, MessageHandler, Updater


class TelegramDialogBot(object):

    def __init__(self, token, responce_handler):
        self.updater = Updater(token=token)
        handler = MessageHandler(Filters.text | Filters.command, self.send_message)
        self.updater.dispatcher.add_handler(handler)
        self.responce_handler = responce_handler

    def start(self):
        self.updater.start_polling()

    def send_message(self, bot, update):
        answer = self.responce_handler(update.message.text, update.message.chat_id)
        if answer:
            update.message.reply_text(answer)
