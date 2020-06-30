import random
import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType


class VkDialogBot(object):

    def __init__(self, token, responce_handler):
        self.vk_session = vk_api.VkApi(token=token)
        self.vk_api = self.vk_session.get_api()
        self.responce_handler = responce_handler

    def start(self):
        longpoll = VkLongPoll(self.vk_session)
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                self.send_message(event)

    def send_message(self, event):
        answer = self.responce_handler(event.text, event.user_id)
        if answer:
            self.vk_api.messages.send(
                user_id=event.user_id,
                message=answer,
                random_id=random.randint(1, 1000)
            )
