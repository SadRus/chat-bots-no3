import logging
import os

from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)


logger = logging.getLogger(__name__)


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте!",
    )


def dialogflow_answer(update: Update, context: CallbackContext):
    text = detect_intent_texts(text=update.message.text)
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=text,
    )


def main():
    load_dotenv()
    logging.basicConfig(
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        level=logging.INFO,
    )
    tg_bot_token = os.getenv('TG_BOT_TOKEN')

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Message handlers
    dispatcher.add_handler(
        MessageHandler(Filters.text & (~Filters.command), dialogflow_answer)
    )

    updater.start_polling()


if __name__ == '__main__':
    main()
