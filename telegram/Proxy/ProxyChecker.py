# -*- coding: utf-8 -*-

from requests import post
from requests.exceptions import RequestException


class ProxyChecker:
    # _instance = None
    _checked_proxies = {}

    # def __new__(cls):
    #     if cls._instance is None:
    #         cls._instance = super(ProxyChecker, cls).__new__(cls)
    #     return cls._instance

    @staticmethod
    def check(proxies: dict) -> bool:
        proxy_key = frozenset(proxies.items())
        print(0)

        if proxy_key in ProxyChecker._checked_proxies:
            return ProxyChecker._checked_proxies[proxy_key]

        print(1)

        try:
            print(3)
            post('https://api.telegram.org/', proxies=proxies)
            result = True
        except RequestException:
            result = False

        ProxyChecker._checked_proxies[proxy_key] = result

        return result
