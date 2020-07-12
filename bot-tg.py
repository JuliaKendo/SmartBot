import os
import logging
import requests
import telegram
import logger_tools
import dialog_tools
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater

logger = logging.getLogger('telegrambot')


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
        answer = self.responce_handler(self.project_id, update.message.chat_id, update.message.text, 'tg-')
        if answer:
            update.message.reply_text(answer)


def main():
    load_dotenv()
    logger_tools.initialize_logger(
        logger,
        os.getenv('TG_LOG_TOKEN'),
        os.getenv('TG_CHAT_ID')
    )
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
        logger.exception(f'{error}')


if __name__ == "__main__":
    main()
