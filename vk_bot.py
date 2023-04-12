import logging
import os
import telegram
import random
import vk_api as vk

from create_parser import create_parser
from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from tg_handlers import TelegramLogsHandler
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger('vk_bot_no3_logger')


def send_dialogflow_answer(event, vk_api, session_id, project_id):
    input_text = event.text
    intent_content = detect_intent_texts(input_text, session_id, project_id)
    if not intent_content['is_fallback']:
        output_text = intent_content['fulfillment_text']
        vk_api.messages.send(
            user_id=event.user_id,
            message=output_text,
            random_id=random.randint(1, 1000),
        )


def main():
    load_dotenv()
    parser = create_parser()
    args = parser.parse_args()

    tg_bot_logger_token = os.getenv('TG_BOT_LOGGER_TOKEN')
    tg_chat_id = os.getenv('TG_CHAT_ID')
    vk_group_token = os.getenv('VK_GROUP_TOKEN')
    project_id = os.getenv('PROJECT_ID')
    session_id = os.getenv('TG_CHAT_ID')

    tg_bot_logger = telegram.Bot(token=tg_bot_logger_token)

    logs_full_path = os.path.join(args.dest_folder, 'vk_bot_no3.log')
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

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('Vk group chat-bot #3 started')

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                send_dialogflow_answer(event, vk_api, session_id, project_id)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
