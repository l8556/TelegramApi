# -*- coding: utf-8 -*-
from rich import print
from os.path import join, expanduser, isfile
from host_tools import File

from .Proxy import Proxy


class ProxyFile:
    # _checked_proxies = {}

    def __init__(self, path: str = None):
        self._default_proxy_file = join(expanduser('~'), '.telegram', 'proxy.json')
        self._proxy_file = self._get_proxy_file(path)

    def _get_proxy_file(self, path: str = None) -> str:
        if isinstance(path, str) and isfile(path):
            return path
        elif isfile(self._default_proxy_file):
            return self._default_proxy_file
        print(f"[red]Proxy configuration file not found")

    @property
    def configs(self) -> dict:
        if self._proxy_file:
            config = File.read_json(self._proxy_file)

            for key in ['login', 'password', 'ip', 'port']:
                if not config.get(key, None):
                    print(f"[red]|ERROR| Empty parameter {key} in proxy.json file")
                    return {}

            proxy = Proxy(login=config['login'], password=config['password'], ip=config['ip'], port=config['port'])
            return proxy.configs

        return {}
