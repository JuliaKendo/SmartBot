import os
import json
import argparse
import dialogflow_v2
import google.api_core.exceptions as exceptions
from dotenv import load_dotenv


def load_intent(intent):
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    client = dialogflow_v2.IntentsClient()
    parent = client.project_agent_path(project_id)
    client.create_intent(parent, intent)


def train_agent():
    project_id = os.getenv('DIALOGFLOW_PROJECT_ID')
    client = dialogflow_v2.AgentsClient()
    parent = client.project_path(project_id)
    client.train_agent(parent)


def get_intent(name, phrase):
    intent = {'display_name': name}
    intent['messages'] = [{
        'text':
            {"text": ['%s' % phrase['answer']]}
    }]
    intent['training_phrases'] = [{'parts': [{'text': f'{question}'}]} for question in phrase['questions']]

    return intent


def main():
    load_dotenv()
    parser = argparse.ArgumentParser(description='Параметры запуска скрипта')
    parser.add_argument('-f', '--file', default='training_phrases.txt', help='Путь к файлу')
    args = parser.parse_args()
    try:
        with open(args.file, 'r') as file_handler:
            training_phrases = json.load(file_handler)

        intents = [get_intent(key, phrase) for key, phrase in training_phrases.items()]
        for intent in intents:
            load_intent(intent)
        train_agent()
    except exceptions.GoogleAPICallError as error:
        print(f'Не удалось обработать запрос по причине: {error}')

    except ValueError as error:
        print(f'Не удалось загрузить тестовые фразы по причине: {error}')

    except FileNotFoundError:
        print('Не найден файл с тренировочными фразами')

    else:
        print('Фразы успешно загружены из файла')


if __name__ == '__main__':
    main()
