### ОБУЧАЕМЫЙ БОТ

Данный бот помогает осуществлять техническую поддержку пользователей и обладает способностью к обучению. Бот работает во взаимодействии с сервисом [Dialog Flow](https://dialogflow.com/), который позволяет обучать скрипт и формировать ответы на запросы пользователей с использованием нейросети. Бот способен отвечать на сообщения пользователей в Telegram и в сообществе, в социальной сети "В Контакте". Скрипт работает в режиме бесконечного цикла, поэтому остановить его выполнение возможно нажав `Ctrl+C`.

Запускают скрипт без параметров
```
python.exe main.py
```	
Перед запуском скрипта настройте следующие переменные окружения:
- `DIALOGFLOW_PROJECT_ID` - идентификатор проекта на сайте [Google.com](https://cloud.google.com/dialogflow/docs/quick/setup).
- `GOOGLE_APPLICATION_CREDENTIALS` - переменная окружения, где лежит путь до файла с ключами, который необходимо создать в соответствии с документацией [Google.com](https://cloud.google.com/docs/authentication/getting-started).
- `TELEGRAM_ACCESS_TOKEN` - переменная для хранения секретного токена бота [telegram](https://core.telegram.org/bots/api), который необходимо создать перед запуском скрипта.
- `TELEGRAM_CHAT_ID` - переменная в которой хранится ID чата текущего пользователя телеграмм. Его можно получить написав `@userinfobot`. 
- `VK_ACCESS_TOKEN` - переменная в которой хранится секретный токен, необходимый для подключения к api сайта [vk.com](http://www.vk.com). У данного ключа обязательно должно быть право отправлять сообщения.
- `LOG_ACCESS_TOKEN` - переменная для хранения секретного токена бота [telegram](https://core.telegram.org/bots/api), который должен быть создан перед запуском скрипта, и используется скриптом для сообщения информации об ошибках.

Данные переменные инициализируются значениями заданными в .env файле.

Информацию о ходе выполнения скрипт отправляет боту telegram, токен которого должен быть указан в соответствующей переменной окружения.

#### КАК УСТАНОВИТЬ

Для установки необходимо создать проект в [Dialog Flow](https://cloud.google.com/dialogflow/docs/quick/setup), затем создать агента в [Dialog Flow](https://cloud.google.com/dialogflow/docs/quick/build-agent), затем создать JSON ключ, необходимый для взаимодействия бота с [Dialog Flow](https://cloud.google.com/dialogflow/docs/quick/setup). 
После этого необходимо отредактировать файл .env, в котором заполнить `DIALOGFLOW_PROJECT_ID`, `GOOGLE_APPLICATION_CREDENTIALS`, `TELEGRAM_ACCESS_TOKEN`, `VK_ACCESS_TOKEN`, `TELEGRAM_CHAT_ID`, `LOG_ACCESS_TOKEN`.
После чего выполняют тренировку агента. Тренировку можно выполнить вручную, или загрузить тренировочные фразы из текстового файла, следующего формата:

```
{
    "Заголовок": {
        "questions": [
            "Вопрос 1",
            "Вопрос 2",
            "Вопрос 3",
            "Вопрос 4"
        ],
        "answer": "Ответ 1"
    }
}

```
Загрузить подготовленный файл можно с помощью команды:

```
python.exe load_training_phrases.py -f [Имя файла]
```	

Python3 должен быть уже установлен. Для установки зависимостей используйте pip (или pip3, если есть конфликт с Python2):

```
pip install -r requirements.txt
```
В составе скрипта присутствует файл `Procfile`, необходимый для деплоя на сервер [HEROKU](https://heroku.com). Файл уже настроен должным образом, поэтому перенос скрипта на сервер выполняется в соответствии с документацией сервера [HEROKU](https://devcenter.heroku.com/articles/git).

#### ЦЕЛЬ ПРОЕКТА

Код написан в образовательных целях, для изучения возможностей чат-ботов, на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org).