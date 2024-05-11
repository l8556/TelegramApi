# -*- coding: utf-8 -*-
from tempfile import gettempdir

from .Proxy import Proxy
from .Send import TelegramRequests, Message, MediaGroup, Document


class Telegram:

    def __init__(
            self,
            token: str = None,
            chat_id: str = None,
            tmp_dir: str = gettempdir(),
            proxy: Proxy = None,
            proxy_file:  str = None,
            max_request_attempts: int = 10,
            interval: int = 5
    ):
        self.tmp_dir = tmp_dir
        self.requests = TelegramRequests(token, chat_id, proxy, proxy_file, max_request_attempts, interval)

    def send_message(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        Message(self.requests, self.tmp_dir).send(message=message, out_msg=out_msg, parse_mode=parse_mode)


    def send_document(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        Document(self.requests, self.tmp_dir).send(document_path, caption, parse_mode)

    def send_media_group(self,
            document_paths: list,
            caption: str = None,
            media_type: str = 'document',
            parse_mode: str = None
    ) -> None:
        """
        :param max_request_attempts:
        :param parse_mode: HTML, Markdown, MarkdownV2
        :param document_paths:
        :param caption:
        :param media_type: types: 'photo', 'video', 'audio', 'document', 'voice', 'animation'
        :return:
        """

        MediaGroup(self.requests).send(document_paths, caption, media_type, parse_mode)
