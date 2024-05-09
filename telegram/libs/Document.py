# -*- coding: utf-8 -*-
import os
from tempfile import gettempdir

from .Caption import Caption
from .Send import Send
from ..utils import File


class Document(Send):

    def send(self, document_path: str, caption: str = '', parse_mode: str = None):
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD

        _data = {"chat_id": self.requests.auth.chat_id, "caption": Caption().prepare(caption), "parse_mode": _parse_mod}
        _file = {"document": open(self.prepare(document_path), 'rb')}

        self.requests.post('sendDocument', data=_data, files=_file)


    def prepare(self, doc_path: str, tmp_dir: str = gettempdir()) -> str:
        if not os.path.isdir(doc_path) or os.path.getsize(doc_path) <= self.__MAX_DOCUMENT_SIZE:
            return doc_path

        archive_path = os.path.join(tmp_dir, f'{os.path.basename(doc_path)}.zip')
        File.compress(doc_path, archive_path)
        return archive_path
