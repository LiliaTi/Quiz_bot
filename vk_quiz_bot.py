import random
import vk_api as vk
from vk_api.longpoll import VkLongPoll, VkEventType
import os
from vk_api.keyboard import VkKeyboard, VkKeyboardColor
import redis
from common import get_questions
import logging


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO
)

logger = logging.getLogger(__name__)


def echo(event, vk_api):
    vk_api.messages.send(
        user_id=event.user_id,
        message=event.text,
        random_id=random.randint(1, 1000)
    )


def handle_new_question_request(event, vk_api, questions, data_base):
    question, answer = random.choice(list(questions.items()))
    data_base.set(event.user_id, answer)
    vk_api.messages.send(
        user_id=event.user_id,
        message=question,
        random_id=random.randint(1, 1000)
    )


def handle_give_up_attempt(event, vk_api, questions, data_base):
    right_answer = data_base.get(event.user_id).decode()
    vk_api.messages.send(
        user_id=event.user_id,
        message='Вот правильный ответ',
        random_id=random.randint(1, 1000)
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message=right_answer,
        random_id=random.randint(1, 1000)
    )
    vk_api.messages.send(
        user_id=event.user_id,
        message='Лови следующий вопрос',
        random_id=random.randint(1, 1000)
    )
    handle_new_question_request(event, vk_api, questions, data_base)


def handle_solution_attempt(event, vk_api, questions, data_base):
    right_answer = data_base.get(event.user_id).decode()
    if event.text.lower() in right_answer.lower():
        vk_api.messages.send(
            user_id=event.user_id,
            message='Привильно! Так держать!',
            random_id=random.randint(1, 1000)
        )

    else:
        vk_api.messages.send(
            user_id=event.user_id,
            message='Неправильно( Попробуешь еще раз?',
            random_id=random.randint(1, 1000)
        )


def main():
    vk_bot_token = os.environ.get('VK_BOT_TOKEN')
    vk_session = vk.VkApi(token=vk_bot_token)
    vk_api = vk_session.get_api()

    questions = get_questions()

    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')
    redis_password = os.environ.get('REDIS_PASSWORD')

    redis_data_base = redis.Redis(host=redis_host,
                                  port=redis_port,
                                  db=0, password=redis_password)

    keyboard = VkKeyboard(one_time=False)

    keyboard.add_button('Новый вопрос', color=VkKeyboardColor.POSITIVE)

    keyboard.add_button('Сдаться', color=VkKeyboardColor.NEGATIVE)

    keyboard.add_line()
    keyboard.add_button('Мой счет', color=VkKeyboardColor.PRIMARY)

    longpoll = VkLongPoll(vk_session)
    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            if event.text == 'Клавиатура':
                vk_api.messages.send(
                    user_id=event.user_id,
                    message='))))',
                    keyboard=keyboard.get_keyboard(),
                    random_id=random.randint(1, 1000)
                )
            elif event.text == 'Новый вопрос':
                handle_new_question_request(event,
                                            vk_api,
                                            questions,
                                            redis_data_base)
            elif event.text == 'Мой счет':
                echo(event, vk_api)

            elif event.text == 'Сдаться':
                handle_give_up_attempt(event,
                                       vk_api,
                                       questions,
                                       redis_data_base)

            else:
                handle_solution_attempt(event,
                                        vk_api,
                                        questions,
                                        redis_data_base)


if __name__ == '__main__':
    main()
