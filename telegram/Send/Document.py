# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from .Caption import Caption
from .Send import Send
from .telegram_request import TelegramRequests
from ..utils import File


class Document(Send):

    def __init__(self, requests: TelegramRequests):
        super().__init__(requests=requests)
        self.caption = Caption()

    def send(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        self.requests.post(
            'sendDocument',
            data=self._generate_data(self.caption.prepare(caption), parse_mode or self._DEFAULT_PARSE_MOD),
            files={ "document": open(self.prepare(document_path), 'rb') }
        )

    def prepare(self, doc_path: str, tmp_dir: str = gettempdir()) -> str:
        if not os.path.isdir(doc_path) or os.path.getsize(doc_path) <= self._MAX_DOCUMENT_SIZE:
            return doc_path

        archive_path = os.path.join(tmp_dir, f'{os.path.basename(doc_path)}.zip')
        File.compress(doc_path, archive_path)
        return archive_path

    def _generate_data(self, caption: str, parse_mode: str) -> dict:
        return {
            "chat_id": self.requests.auth.chat_id,
            "caption": self.caption.prepare(caption),
            "parse_mode": parse_mode
        }
