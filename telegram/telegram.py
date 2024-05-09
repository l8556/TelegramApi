# -*- coding: utf-8 -*-
from json import dumps
from tempfile import gettempdir
from os.path import basename
from rich import print
from .config import Config

from host_tools import File

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
        self.requests = TelegramRequests(token, chat_id, proxy, proxy_file, max_request_attempts, interval)
        self.tmp_dir = tmp_dir

    def send_message(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        Message(self.requests).send(message, out_msg, parse_mode)


    def send_document(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        Document(self.requests).send(document_path, caption, parse_mode)

    def send_media_group(self,
            document_paths: list,
            caption: str = None,
            media_type: str = 'document',
            parse_mode: str = None
    ) -> None:
        """
        :param parse_mode: HTML, Markdown, MarkdownV2
        :param document_paths:
        :param caption:
        :param media_type: types: 'photo', 'video', 'audio', 'document', 'voice', 'animation'
        :return:
        """
        MediaGroup(self.requests).send(document_paths, caption, media_type, parse_mode)
