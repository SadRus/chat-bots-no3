import logging
import os
import telegram

from create_parser import create_parser
from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from functools import partial
from telegram import Update
from telegram.ext import (
    CallbackContext,
    CommandHandler,
    Filters,
    MessageHandler,
    Updater,
)
from tg_handlers import TelegramLogsHandler


logger = logging.getLogger('tg_bot_no3_logger')


def start(update: Update, context: CallbackContext):
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text="Здравствуйте!",
    )


def send_dialogflow_answer(
        update: Update,
        context: CallbackContext,
        session_id,
        project_id,
):
    input_text = update.message.text
    intent_content = detect_intent_texts(input_text, session_id, project_id)
    output_text = intent_content['fulfillment_text']
    context.bot.send_message(
        chat_id=update.effective_chat.id,
        text=output_text,
    )


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    tg_bot_token = os.getenv('TG_BOT_TOKEN')
    tg_bot_logger_token = os.getenv('TG_BOT_LOGGER_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    send_dialogflow_answer_partial = partial(
        send_dialogflow_answer,
        project_id=os.getenv('PROJECT_ID'),
        session_id=os.getenv('TG_CHAT_ID'),
    )

    tg_bot_logger = telegram.Bot(token=tg_bot_logger_token)

    logs_full_path = os.path.join(args.dest_folder, 'tg_bot_no3.log')
    os.makedirs(args.dest_folder, exist_ok=True)
    logging.basicConfig(
        level=logging.INFO,
        filename=logs_full_path,
        filemode='w',
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    )
    logger.setLevel(logging.INFO)
    handler = TelegramLogsHandler(
        logs_full_path,
        tg_bot=tg_bot_logger,
        chat_id=tg_chat_id,
        maxBytes=args.max_bytes,
        backupCount=args.backup_count,
    )
    logger.addHandler(handler)

    updater = Updater(tg_bot_token)
    dispatcher = updater.dispatcher

    # Command handlers
    dispatcher.add_handler(CommandHandler('start', start))

    # Message handlers
    dispatcher.add_handler(
        MessageHandler(
            Filters.text & (~Filters.command),
            send_dialogflow_answer_partial,
        )
    )
    try:
        updater.start_polling()
        logger.info('Telegram chat-bot #3 @vo1ce_c1ty_bot started')
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
