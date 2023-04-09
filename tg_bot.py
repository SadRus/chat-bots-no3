import logging
import os

from create_parser import create_parser
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
    parser = create_parser()
    args = parser.parse_args()

    logs_full_path = os.path.join(args.dest_folder, 'tg_bot_no3.log')
    os.makedirs(args.dest_folder, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=logs_full_path,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        filename=logs_full_path,
        maxBytes=args.max_bytes,
        backupCount=args.backup_count,
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
