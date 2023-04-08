import os
import random
import vk_api as vk

from detect_intent_text import detect_intent_texts
from dotenv import load_dotenv
from vk_api.longpoll import VkLongPoll, VkEventType


def echo(event, vk_api):
    incoming_text = event.text
    outgoing_text = detect_intent_texts(incoming_text)
    vk_api.messages.send(
        user_id=event.user_id,
        message=outgoing_text,
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
            echo(event, vk_api)


if __name__ == '__main__':
    main()
