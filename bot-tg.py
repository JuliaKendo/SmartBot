import os
import logging
import requests
import telegram
import dialog_tools
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger('telegrambot')


class NotificationLogHandler(logging.Handler):

    def __init__(self, token, chat_id):
        super().__init__()
        self.token = token
        self.chat_id = chat_id

    def emit(self, record):
        log_entry = self.format(record)
        if log_entry:
            bot = telegram.Bot(token=self.token)
            bot.sendMessage(chat_id=self.chat_id, text=log_entry)


class TgDialogBot(object):

    def __init__(self, token, project_id, responce_handler):
        self.updater = Updater(token=token)
        self.project_id = project_id
        handler = MessageHandler(Filters.text | Filters.command, self.send_message)
        self.updater.dispatcher.add_handler(handler)
        self.responce_handler = responce_handler

    def start(self):
        self.updater.start_polling()

    def send_message(self, bot, update):
        answer = self.responce_handler(self.project_id, update.message.text, tg_session_id=update.message.chat_id)
        if answer:
            update.message.reply_text(answer)


def initialize_logger():
    handler = NotificationLogHandler(os.getenv('TG_LOG_TOKEN'), os.getenv('TG_CHAT_ID'))
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def main():
    load_dotenv()
    initialize_logger()
    logger.info('telegram bot launched')
    try:
        bot = TgDialogBot(
            os.getenv('TG_ACCESS_TOKEN'),
            os.getenv('DIALOGFLOW_PROJECT_ID'),
            dialog_tools.get_answer
        )
        bot.start()

    except (
        telegram.TelegramError,
        requests.exceptions.HTTPError,
        KeyError, TypeError, ValueError
    ) as error:
        logger.error(f'{error}', exc_info=True)


if __name__ == "__main__":
    main()
