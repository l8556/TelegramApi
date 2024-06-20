# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from ..config import Config
from ..utils import File

from .Document import Document
from .Send import Send
from .tools import TelegramRequests


class Message(Send):
    _DEFAULT_PARSE_MOD: str = Config.DEFAULT_PARSE_MOD
    _MAX_MESSAGE_LENGTH: int = Config.MAX_MESSAGE_LENGTH

    def __init__(self, requests: TelegramRequests, tmp_dir: str = gettempdir()):
        self.requests = requests
        self.document = Document(self.requests)
        self.tmp_dir = tmp_dir

    def send(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        print(message) if out_msg else ...

        if len(message) > self._MAX_MESSAGE_LENGTH:
            document_path = self.make_doc(message=message)
            self.document.send(document_path, caption=message)
            return File.delete(document_path)

        self.requests.post(
            mode='sendMessage',
            data={
                "chat_id": self.requests.auth.chat_id,
                "text": message,
                "parse_mode": parse_mode or self._DEFAULT_PARSE_MOD
            }
        )

    @staticmethod
    def make_doc(message: str, name: str = 'message.txt') -> str:
        doc_path = os.path.join(self.tmp_dir, name)

        with open(doc_path, 'w') as file:
            file.write(message)

        return doc_path
