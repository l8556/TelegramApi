# -*- coding: utf-8 -*-
from telegram.libs.telegram_request import TelegramRequests


class Message:

    def __init__(self, requests: TelegramRequests):
        self.requests = requests

    def send(self):
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD
        print(message) if out_msg else ...

        if len(message) > self.__MAX_MESSAGE_LENGTH:
            document = self.msg.make_doc(message=message)
            self.send_document(document, caption=message)
            return File.delete(document, stdout=False)

        message_data = { "chat_id": chat_id, "text": message, "parse_mode": _parse_mod }
        self.requests.post('sendMessage', data=message_data, tg_log=False)
