import os
import random
import vk_api as vk

from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


def dialogflow_answer(event, vk_api):
    input_text = event.text
    intent_content = detect_intent_texts(input_text)
    output_text = intent_content['fulfillment_text']
    if intent_content['is_fallback']:
        output_text = None
    vk_api.messages.send(
        user_id=event.user_id,
        message=output_text,
        random_id=random.randint(1, 1000),
    )


def main():
    load_dotenv()

    vk_group_token = os.getenv('VK_GROUP_TOKEN')

    vk_session = vk.VkApi(token=vk_group_token)
    vk_api = vk_session.get_api()
    longpoll = VkLongPoll(vk_session)

    for event in longpoll.listen():
        if event.type == VkEventType.MESSAGE_NEW and event.to_me:
            dialogflow_answer(event, vk_api)


if __name__ == '__main__':
    main()
