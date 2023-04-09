import logging
import os
import random
import vk_api as vk

from create_parser import create_parser
from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from vk_api.longpoll import VkLongPoll, VkEventType


logger = logging.getLogger('vk_bot_no3_logger')


def dialogflow_answer(event, vk_api):
    input_text = event.text
    intent_content = detect_intent_texts(input_text)
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

    logs_full_path = os.path.join(args.dest_folder, 'vk_bot_no3.log')
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

    vk_group_token = os.getenv('VK_GROUP_TOKEN')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)
    logger.info('VK_bot_no3 started')

    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                dialogflow_answer(event, vk_api)
    except Exception as e:
        logger.exception(e)


if __name__ == '__main__':
    main()
