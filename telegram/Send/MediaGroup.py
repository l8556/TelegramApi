# -*- coding: utf-8 -*-
from os.path import basename
from json import dumps

from .Document import Document
from .Caption import Caption
from .Message import Message
from .Send import Send
from .telegram_request import TelegramRequests


class MediaGroup(Send):

    def __init__(self, requests: TelegramRequests):
        super().__init__(requests=requests)
        self.message = Message(self.requests)
        self.document = Document(self.requests)
        self.caption = Caption()

    def send(
        self,
        document_paths: list,
        caption: str = None,
        media_type: str = 'document',
        parse_mode: str = None,
        max_request_attempts: int = 10
    ) -> None:

        if not document_paths:
            return self.message.send(f"No files to send. {caption if caption else ''}", out_msg=True)

        if caption and len(caption) > self._MAX_CAPTCHA_LENGTH:
            document_paths.append(self.message.make_doc(caption, 'full_caption.txt'))

        for chung in self._get_group_chunks(document_paths):
            while max_request_attempts > 0:
                files, data = self._get_data(chung, media_type, caption, parse_mode or self._DEFAULT_PARSE_MOD)

                if self.requests.post('sendMediaGroup', data=data, files=files):
                    break

                max_request_attempts -= 1

    def _get_data(self, document_paths: list, media_type: str, caption: str, parse_mode: str) -> tuple[dict, dict]:
        files, media = {}, []

        for doc_path in document_paths:
            files[basename(doc_path)] = open(self.document.prepare(doc_path), 'rb')
            media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))

        media[-1]['caption'] = self.caption.prepare(caption) if caption is not None else ''
        media[-1]['parse_mode'] = parse_mode

        return files, {'chat_id': self.requests.auth.chat_id, 'media': dumps(media)}

    def _get_group_chunks(self, document_paths: list) -> list:
        length = self._MAX_MEDIA_GROUP_LENGTH
        return [document_paths[i:i + length] for i in range(0, len(document_paths), length)]
