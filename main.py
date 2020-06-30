import os
import logging
import requests
import dialogflow_v2
from dotenv import load_dotenv
from telegram_logger import NotificationLogHandler
import smart_telegram_bot
import smart_vk_bot
from telegram import TelegramError
from vk_api import VkApiError, ApiHttpError, AuthError

LANGUAGE_CODE = 'ru-RU'
logger = logging.getLogger('smartbot')


def get_answer_into_vk(text, session_id):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    session_client = dialogflow_v2.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow_v2.types.TextInput(text=text, language_code=LANGUAGE_CODE)
    query_input = dialogflow_v2.types.QueryInput(text=text_input)

    response = session_client.detect_intent(session=session, query_input=query_input)

    return response.query_result.fulfillment_text if not response.query_result.intent.is_fallback else None


def get_answer_into_telegram(text, session_id):
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
    logger.info('Бот запущен')
    try:
        telegram_bot = smart_telegram_bot.TelegramDialogBot(os.getenv('TELEGRAM_ACCESS_TOKEN'), get_answer_into_telegram)
        telegram_bot.start()
        vk_bot = smart_vk_bot.VkDialogBot(os.getenv('VK_ACCESS_TOKEN'), get_answer_into_vk)
        vk_bot.start()

    except (VkApiError, ApiHttpError, AuthError) as error:
        logger.error(f'{error}', exc_info=True)

    except TelegramError as error:
        logger.error(f'{error}', exc_info=True)

    except requests.exceptions.HTTPError as error:
        logger.error(f'{error}', exc_info=True)

    except (KeyError, TypeError, ValueError) as error:
        logger.error(f'{error}', exc_info=True)


if __name__ == "__main__":
    main()
