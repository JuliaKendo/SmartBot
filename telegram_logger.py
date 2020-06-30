import logging
import telegram


class NotificationLogHandler(logging.Handler):

    def __init__(self, token, chat_id):
        logging.Handler.__init__(self)
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        if log_entry:
            bot = telegram.Bot(token=self.token)
            bot.sendMessage(chat_id=self.chat_id, text=log_entry)
