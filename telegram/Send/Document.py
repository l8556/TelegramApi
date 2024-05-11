# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from .Send import Send
from .tools import TelegramRequests, Caption
from ..config import Config
from ..utils import File


class Document(Send):
    _DEFAULT_PARSE_MOD: str = Config.DEFAULT_PARSE_MOD
    _MAX_DOCUMENT_SIZE: int = Config.MAX_DOCUMENT_SIZE

    def __init__(self, requests: TelegramRequests, tmp_dir: str = gettempdir()):
        self.requests = requests
        self.caption = Caption()
        self.tmp_dir = tmp_dir

    def send(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        self.requests.post(
            'sendDocument',
            data=self._generate_data(self.caption.prepare(caption), parse_mode or self._DEFAULT_PARSE_MOD),
            files={ "document": open(self.prepare(document_path), 'rb') }
        )

    def prepare(self, doc_path: str) -> str:
        if not os.path.isdir(doc_path) or os.path.getsize(doc_path) <= self._MAX_DOCUMENT_SIZE:
            return doc_path

        archive_path = os.path.join(self.tmp_dir, f'{os.path.basename(doc_path)}.zip')
        File.compress(doc_path, archive_path)
        return archive_path

    def _generate_data(self, caption: str, parse_mode: str) -> dict:
        return {
            "chat_id": self.requests.auth.chat_id,
            "caption": self.caption.prepare(caption),
            "parse_mode": parse_mode
        }
