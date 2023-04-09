import logging
import os

from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


logger = logging.getLogger('tg_bot_logger')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте!",
    )


def dialogflow_answer(update: Update, context: CallbackContext):
    input_text = update.message.text
    intent_content = detect_intent_texts(input_text)
    output_text = intent_content['fulfillment_text']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=output_text,
    )


def main():
    load_dotenv()
    logging.basicConfig(
        level=logging.INFO,
        filename='tg_bot.log',
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        filename='tg_bot.log',
        maxBytes=200,
        backupCount=1,
    )
    logger.addHandler(handler)

    tg_bot_token = os.getenv('TG_BOT_TOKEN')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Message handlers
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), dialogflow_answer)
    )
    try:
        updater.start_polling()
        logger.info('Bot started')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
