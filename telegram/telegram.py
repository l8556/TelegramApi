# -*- coding: utf-8 -*-
import time
from json import dumps
from requests import post
from tempfile import gettempdir
from os.path import join, getsize, basename, isdir
from rich import print

from host_tools import File, Dir
from urllib3 import HTTPSConnectionPool
from urllib3.exceptions import NewConnectionError

from .Auth import Auth
from .Proxy import Proxy, ProxyFile


class Telegram:
    __MAX_DOCUMENT_SIZE: int = 50_000_000
    __MAX_CAPTCHA_LENGTH: int = 1000
    __DEFAULT_PARSE_MOD: str = 'Markdown'

    def __init__(
            self,
            token: str = None,
            chat_id: str = None,
            tmp_dir: str = gettempdir(),
            proxy: Proxy = None,
            proxy_file:  str = None
    ):
        self.auth = Auth(token=token, chat_id=chat_id)
        self.tmp_dir = tmp_dir
        self.proxies: dict = self._get_proxies(proxy, proxy_file)
        Dir.create(self.tmp_dir, stdout=False)

    @staticmethod
    def _get_proxies(proxy: Proxy = None, proxy_file: "True | str" = None) -> dict:
        if isinstance(proxy, Proxy):
            return proxy.get_param()
        elif proxy_file:
            return ProxyFile(proxy_file).get_config()
        return {}

    def send_message(self, message: str, out_msg: bool = False, parse_mode: str = None) -> None:
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD
        print(message) if out_msg else ...

        if len(message) > 4096:
            document = self._make_massage_doc(message=message)
            self.send_document(document, caption=self._prepare_caption(message))
            return File.delete(document, stdout=False)

        self._request(
            f"https://api.telegram.org/bot{self.auth.token}/sendMessage",
            data={
                "chat_id": self.auth.chat_id,
                "text": message,
                "parse_mode": _parse_mod
            },
            tg_log=False
        )

    def send_document(self, document_path: str, caption: str = '', parse_mode: str = None) -> None:
        _parse_mod = parse_mode if parse_mode else self.__DEFAULT_PARSE_MOD
        self._request(
            f"https://api.telegram.org/bot{self.auth.token}/sendDocument",
            data={"chat_id": self.auth.chat_id, "caption": self._prepare_caption(caption), "parse_mode": _parse_mod},
            files={"document": open(self._prepare_documents(document_path), 'rb')}
        )

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
        files, media = {}, []

        if not document_paths:
            return self.send_message(f"No files to send. {caption if caption else ''}", out_msg=True)

        if caption and len(caption) > self.__MAX_CAPTCHA_LENGTH:
            document_paths.append(self._make_massage_doc(caption, 'caption.txt'))

        for doc_path in document_paths:
            files[basename(doc_path)] = open(self._prepare_documents(doc_path), 'rb')
            media.append(dict(type=media_type, media=f'attach://{basename(doc_path)}'))

        media[-1]['caption'] = self._prepare_caption(caption) if caption is not None else ''
        media[-1]['parse_mode'] = _parse_mod

        self._request(
            f'https://api.telegram.org/bot{self.auth.token}/sendMediaGroup',
            data={'chat_id': self.auth.chat_id, 'media': dumps(media)},
            files=files
        )

    @staticmethod
    def escape_special_characters(text: str, special_characters: str) -> str:
        escaped_string = ""

        for char in text:
            if char in special_characters:
                escaped_string += '\\' + char
            else:
                escaped_string += char

        return escaped_string

    def _request(self, url: str, data: dict, files: dict = None, tg_log: bool = True, num_tries: int = 10) -> None:
        if self.auth.token and self.auth.chat_id:
            while num_tries > 0:
                try:
                    print(f"[red]|INFO| The message to Telegram will be sent via proxy") if self.proxies else ...
                    response = post(url, data=data, files=files, proxies=self.proxies)

                    if response.status_code == 200:
                        return

                    print(f"Error when sending to telegram: {response.json()}")

                    if response.status_code == 429:
                        timeout = response.json().get('parameters', {}).get('retry_after', 10) + 1
                        print(f"Retry after: {timeout}")
                        time.sleep(timeout)

                except (HTTPSConnectionPool, NewConnectionError) as e:
                    print(f"|WARNING| Impossible to send: {data}. Error: {e}\n timeout: 20 sec")
                    self.send_message(f"|WARNING| Impossible to send: {data}. Error: {e}") if tg_log else ...
                    time.sleep(20)

                finally:
                    num_tries -= 1

    def _prepare_documents(self, doc_path: str) -> str:
        if not isdir(doc_path) or getsize(doc_path) <= self.__MAX_DOCUMENT_SIZE:
            return doc_path
        archive_path = join(self.tmp_dir, f'{basename(doc_path)}.zip')
        File.compress(doc_path, archive_path)
        return archive_path

    def _prepare_caption(self, caption: str) -> str:
        return caption[:self.__MAX_CAPTCHA_LENGTH]

    def _make_massage_doc(self, message: str, name: str = 'message.txt') -> str:
        doc_path = join(self.tmp_dir, name)
        File.write(doc_path, message)
        return doc_path
