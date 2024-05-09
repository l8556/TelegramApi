# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC

from telegram.config import Config
from .telegram_request import TelegramRequests

class Send(ABC):
    _MAX_CAPTCHA_LENGTH: int = Config.MAX_CAPTCHA_LENGTH
    _MAX_MESSAGE_LENGTH: int = Config.MAX_MESSAGE_LENGTH
    _DEFAULT_PARSE_MOD: str = Config.DEFAULT_PARSE_MOD
    _MAX_DOCUMENT_SIZE: int = Config.MAX_DOCUMENT_SIZE

    def __init__(self, requests: TelegramRequests):
        self.requests = requests

    @abstractmethod
    def send(self, *args, **kwargs) -> None: ...
