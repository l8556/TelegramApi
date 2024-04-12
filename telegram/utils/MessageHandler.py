# -*- coding: utf-8 -*-
import os
from host_tools.utils import File, Dir
from ..config import Config


class MessageHandler:

    def __init__(self, tmp_dir: str):
        self.tmp_dir = tmp_dir
        self.captcha_length = Config.MAX_CAPTCHA_LENGTH
        Dir.create(self.tmp_dir, stdout=False)

    def prepare_documents(self, doc_path: str) -> str:
        if not os.path.isdir(doc_path) or os.path.getsize(doc_path) <= Config.MAX_DOCUMENT_SIZE:
            return doc_path

        archive_path = os.path.join(self.tmp_dir, f'{os.path.basename(doc_path)}.zip')
        File.compress(doc_path, archive_path)
        return archive_path

    def prepare_caption(self, caption: str, ) -> str:
        return caption[:self.captcha_length]

    def make_doc(self, message: str, name: str = 'message.txt') -> str:
        doc_path = os.path.join(self.tmp_dir, name)

        with open(doc_path, 'w') as file:
            file.write(message)

        return doc_path
