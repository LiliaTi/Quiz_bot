# Чатботы для проведения викторины

Данный проект реализует двух ботов vk и telegram, которые проводят для пользователя викторину: задают ему вопросы на общую эрудицию, сообщают правилен ли ответ. Также реализована возможность "сдаться", когда боты присылают правильный ответ.

## Пример использования

Telegram

[![tg-quiz-bot.gif](https://s2.gifyu.com/images/tg-quiz-bot.gif)](https://gifyu.com/image/UEQD)


VK

[![vk-quiz-bot.gif](https://s2.gifyu.com/images/vk-quiz-bot.gif)](https://gifyu.com/image/UEQO)

## Как установить

### На локальной машине

Создайте в корне директории файл .env со следующими переменными
```python
TG_BOT_TOKEN=YOUR_TG_BOT_TOKEN
REDIS_HOST=YOUR_REDIS_HOST
REDIS_PORT=YOUR_REDIS_PORT
REDIS_PASSWORD=YOUR_REDIS_PASSWORD
VK_BOT_TOKEN=YOUR_VK_BOT_TOKEN
```

оздайте группу vk, в вашей группе кликните Управление -> Работа с API -> Создать ключ (разрешите отправку сообщений)

Создайте бота телеграм с помощью [@BotFather](https://telegram.me/botfather). Получите токен вашего бота

Python3 должен быть уже установлен. Затем используйте pip (или pip3, есть есть конфликт с Python2) для установки зависимостей:

```python
pip install -r requirements.txt
```
Запустите скрипты следующими командами:
```python
python vk_quiz_bot.py
```
```python
python tg_quiz_bot.py
```

### Деплой на Heroku

Склонируйте репозиторий, войдите или зарегистрируйтесь на [Heroku](https://dashboard.heroku.com)

Создайте новое приложение Heroku, во вкладке Deploy подключите ваш github аккаунт.Выберите нужный репозиторий.

Во вкладке Settings установите переменные окружения как Config Vars.

Активируйте бота на вкладке Resourses.