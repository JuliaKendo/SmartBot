import os
import logging
import requests
import random
import dialog_tools
import logger_tools
from vk_api import VkApi, VkApiError, ApiHttpError, AuthError
from vk_api.longpoll import VkLongPoll, VkEventType
from dotenv import load_dotenv

logger = logging.getLogger('vkbot')


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
        answer = self.response_handler(self.project_id, event.user_id, event.text, 'vk-')
        if answer:
            self.vk_api.messages.send(
                user_id=event.user_id,
                message=answer,
                random_id=random.randint(1, 1000)
            )


def main():
    load_dotenv()
    logger_tools.initialize_logger(
        logger,
        os.getenv('TG_LOG_TOKEN'),
        os.getenv('TG_CHAT_ID')
    )
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
        logger.exception(f'{error}')


if __name__ == "__main__":
    main()
