# -*- coding: utf-8 -*-
from json import dumps
from tempfile import gettempdir
from os.path import basename
from rich import print
from .config import Config
from .utils import MessageHundler

from host_tools import File

from .Proxy import Proxy
from telegram.libs.telegram_request import TelegramRequests


class Telegram:
    __MAX_CAPTCHA_LENGTH: int = Config.MAX_CAPTCHA_LENGTH
    __MAX_MESSAGE_LENGTH: int = Config.MAX_MESSAGE_LENGTH
    __DEFAULT_PARSE_MOD: str = Config.DEFAULT_PARSE_MOD

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
        self.interval = interval
        self.max_request_attempts = max_request_attempts
        self.requests = TelegramRequests(token, chat_id, proxy, proxy_file, self.max_request_attempts, self.interval)
        self.tmp_dir = tmp_dir
        self.msg = MessageHundler(self.tmp_dir)

    def send_message(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD
        print(message) if out_msg else ...

        if len(message) > self.__MAX_MESSAGE_LENGTH:
            document = self.msg.make_doc(message=message)
            self.send_document(document, caption=message)
            return File.delete(document, stdout=False)

        message_data = { "chat_id": self.requests.auth.chat_id, "text": message, "parse_mode": _parse_mod }
        self.requests.post('sendMessage', data=message_data, tg_log=False)


    def send_document(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD

        _data = { "chat_id": self.requests.auth.chat_id, "caption": MessageHundler.prepare_caption(caption), "parse_mode": _parse_mod}
        _file = { "document": open(self.msg.prepare_documents(document_path), 'rb') }

        self.requests.post('sendDocument', data=_data, files=_file)

    def send_media_group(
            self,
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
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD

        if not document_paths:
            return self.send_message(f"No files to send. {caption if caption else ''}", out_msg=True)

        if caption and len(caption) > self.__MAX_CAPTCHA_LENGTH:
            document_paths.append(self.msg.make_massage_doc(caption, 'caption.txt'))

        _max_attempts = self.max_request_attempts

        while _max_attempts > 0:
            files, media = {}, []
            for doc_path in document_paths:
                files[basename(doc_path)] = open(self.msg.prepare_documents(doc_path), 'rb')
                media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))

            media[-1]['caption'] = self.msg.prepare_caption(caption) if caption is not None else ''
            media[-1]['parse_mode'] = _parse_mod

            media_group_data = { 'chat_id': self.requests.auth.chat_id, 'media': dumps(media) }

            if self.requests.post('sendMediaGroup', data=media_group_data, files=files):
                break

            _max_attempts -= 1
