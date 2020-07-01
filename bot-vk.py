import os
import logging
import requests
import telegram
import dialogflow_v2
import random
from vk_api import VkApi, VkApiError, ApiHttpError, AuthError
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger('vkbot')


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


class VkDialogBot(object):

    def __init__(self, token, responce_handler):
        self.vk_session = VkApi(token=token)
        self.vk_api = self.vk_session.get_api()
        self.responce_handler = responce_handler

    def start(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.send_message(event)

    def send_message(self, event):
        answer = self.responce_handler(event.text, event.user_id)
        if answer:
            self.vk_api.messages.send(
                user_id=event.user_id,
                message=answer,
                random_id=random.randint(1, 1000)
            )


def get_answer(text, session_id):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow_v2.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text if not response.query_result.intent.is_fallback else None


def initialize_logger():
    handler = NotificationLogHandler(os.environ.get('LOG_ACCESS_TOKEN'), os.environ.get('TELEGRAM_CHAT_ID'))
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def main():
    load_dotenv()
    initialize_logger()
    logger.info('vk bot launched')
    try:
        vk_bot = VkDialogBot(os.getenv('VK_ACCESS_TOKEN'), get_answer)
        vk_bot.start()

    except (VkApiError, ApiHttpError, AuthError) as error:
        logger.error(f'{error}', exc_info=True)

    except requests.exceptions.HTTPError as error:
        logger.error(f'{error}', exc_info=True)

    except (KeyError, TypeError, ValueError) as error:
        logger.error(f'{error}', exc_info=True)


if __name__ == "__main__":
    main()
