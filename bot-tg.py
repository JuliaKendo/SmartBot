import os
import logging
import requests
import telegram
import dialogflow_v2
from dotenv import load_dotenv
from telegram.ext import Filters, MessageHandler, Updater

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger('telegrambot')


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


def get_answer(text, session_id):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow_v2.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text


def initialize_logger():
    handler = NotificationLogHandler(os.environ.get('LOG_ACCESS_TOKEN'), os.environ.get('TELEGRAM_CHAT_ID'))
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def main():
    load_dotenv()
    initialize_logger()
    logger.info('telegram bot launched')
    try:
        bot = TelegramDialogBot(os.getenv('TELEGRAM_ACCESS_TOKEN'), get_answer)
        bot.start()

    except telegram.TelegramError as error:
        logger.error(f'{error}', exc_info=True)

    except requests.exceptions.HTTPError as error:
        logger.error(f'{error}', exc_info=True)

    except (KeyError, TypeError, ValueError) as error:
        logger.error(f'{error}', exc_info=True)


if __name__ == "__main__":
    main()
