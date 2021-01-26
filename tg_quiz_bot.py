import logging
from telegram.ext import (Updater, CommandHandler, MessageHandler,
                          Filters, CallbackContext, RegexHandler,
                          ConversationHandler)
import telegram
import os
from common import get_questions
import random
from functools import partial
import redis
from enum import Enum


logger = logging.getLogger(__name__)

State = Enum('State', 'QUESTION SOLUTION')


def start(update, context):
    update.message.reply_text('Привет!Я бот для викторины:)')
    custom_keyboard = [['Новый вопрос', 'Сдаться'], ['Мой счет']]
    reply_markup = telegram.ReplyKeyboardMarkup(custom_keyboard)
    context.bot.sendMessage(chat_id=update.message.chat_id,
                            text=':))))))',
                            reply_markup=reply_markup)
    return State.QUESTION


def handle_new_question_request(update, context, questions, data_base):
    user = update.message.from_user
    question, answer = random.choice(list(questions.items()))
    data_base.set(f'tg-{user.id}', answer)
    update.message.reply_text(question)
    return State.SOLUTION


def handle_give_up_attempt(update, context, questions, data_base):
    user = update.message.from_user
    right_answer = data_base.get(f'tg-{user.id}').decode()
    update.message.reply_text(f'Вот правильный ответ.\n{right_answer}\nЛови следующий вопрос')
    handle_new_question_request(update, context, questions, data_base)


def handle_solution_attempt(update, context, questions, data_base):
    user = update.message.from_user
    right_answer = data_base.get(f'tg-{user.id}').decode()
    if update.message.text.lower() in right_answer.lower():
        context.bot.sendMessage(chat_id=update.message.chat_id,
                                text='Привильно! Так держать!')
        return State.QUESTION
    else:
        context.bot.sendMessage(chat_id=update.message.chat_id,
                                text='Неправильно :( Попробуешь еще раз?')
        return State.SOLUTION


def cancel(update, context):
    user = update.message.from_user
    logger.info(
        f"User {user.first_name} {user.last_name} canceled the conversation.")
    update.message.reply_text('Давай, до скорого',
                              reply_markup=telegram.ReplyKeyboardRemove())
    return ConversationHandler.END


def main():
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO
    )

    logger.info("Start TG bot")
    questions = get_questions()

    tg_bot_token = os.environ.get('TG_BOT_TOKEN')
    redis_host = os.environ.get('REDIS_HOST')
    redis_port = os.environ.get('REDIS_PORT')
    redis_password = os.environ.get('REDIS_PASSWORD')

    redis_data_base = redis.Redis(host=redis_host,
                                  port=redis_port,
                                  db=0, password=redis_password)

    updater = Updater(tg_bot_token, use_context=True)

    send_question = partial(handle_new_question_request,
                            questions=questions,
                            data_base=redis_data_base)

    estimate_answer = partial(handle_solution_attempt,
                              questions=questions,
                              data_base=redis_data_base)

    send_answer = partial(handle_give_up_attempt,
                          questions=questions,
                          data_base=redis_data_base)
    dispatcher = updater.dispatcher

    conv_handler = ConversationHandler(
        entry_points=[CommandHandler('start', start)],
        states={
            State.QUESTION: [RegexHandler('^(Новый вопрос)$', send_question)],

            State.SOLUTION: [RegexHandler('^(Сдаться)$', send_answer),
                             MessageHandler(Filters.text & ~Filters.text(['Сдаться', 'Новый вопрос', 'Мой счет']), estimate_answer)]
        },

        fallbacks=[CommandHandler('cancel', cancel)]
    )

    dispatcher.add_handler(conv_handler)
    updater.start_polling()

    updater.idle()


if __name__ == '__main__':
    main()
