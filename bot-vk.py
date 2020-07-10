import os
import logging
import requests
import telegram
import random
import dialog_tools
from vk_api import VkApi, VkApiError, ApiHttpError, AuthError
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger('vkbot')


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


class VkDialogBot(object):

    def __init__(self, token, project_id, response_handler):
        self.vk_session = VkApi(token=token)
        self.project_id = project_id
        self.vk_api = self.vk_session.get_api()
        self.response_handler = response_handler

    def start(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.send_message(event)

    def send_message(self, event):
        answer = self.response_handler(self.project_id, event.text, vk_session_id=event.user_id)
        if answer:
            self.vk_api.messages.send(
                user_id=event.user_id,
                message=answer,
                random_id=random.randint(1, 1000)
            )


def initialize_logger():
    handler = NotificationLogHandler(os.getenv('TG_LOG_TOKEN'), os.getenv('TG_CHAT_ID'))
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.DEBUG)


def main():
    load_dotenv()
    initialize_logger()
    logger.info('vk bot launched')
    try:
        vk_bot = VkDialogBot(
            os.getenv('VK_ACCESS_TOKEN'),
            os.getenv('DIALOGFLOW_PROJECT_ID'),
            dialog_tools.get_answer
        )
        vk_bot.start()

    except (
        requests.exceptions.HTTPError,
        VkApiError, ApiHttpError, AuthError,
        KeyError, TypeError, ValueError
    ) as error:
        logger.error(f'{error}', exc_info=True)


if __name__ == "__main__":
    main()
