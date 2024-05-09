# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from ..utils import File

from .Document import Document
from .Send import Send
from .telegram_request import TelegramRequests


class Message(Send):

    def __init__(self, requests: TelegramRequests):
        super().__init__(requests=requests)
        self.document = Document(self.requests)

    def send(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        _parse_mod = parse_mode if parse_mode else self._DEFAULT_PARSE_MOD
        print(message) if out_msg else ...

        if len(message) > self.__MAX_MESSAGE_LENGTH:
            document_path = self.make_doc(message=message)
            self.document.send(document_path, caption=message)
            return File.delete(document_path)

        message_data = {"chat_id": self.requests.auth.chat_id, "text": message, "parse_mode": _parse_mod}
        self.requests.post('sendMessage', data=message_data, tg_log=False)

    @staticmethod
    def make_doc(message: str, name: str = 'message.txt', tmp_dir: str = gettempdir()) -> str:
        doc_path = os.path.join(tmp_dir, name)

        with open(doc_path, 'w') as file:
            file.write(message)

        return doc_path
