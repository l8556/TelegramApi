# -*- coding: utf-8 -*-
from telegram.config import Config


class Caption:

    def __init__(self):
        self.captcha_length = Config.MAX_CAPTCHA_LENGTH

    def prepare(self, caption: str) -> str:
        return caption[:self.captcha_length]
