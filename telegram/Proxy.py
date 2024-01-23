# -*- coding: utf-8 -*-
from os.path import join, expanduser, isfile
from rich import print
from host_tools import File, singleton


class Proxy:
    def __init__(self, login: str, password: str, ip: str, port: str):
        self.login = login
        self.password = password
        self.ip = ip
        self.port = port

    def get_param(self) -> dict:
        proxy = f"http://{self.login}:{self.password}@{self.ip}:{self.port}"
        return  {'http': proxy, 'https': proxy}

@singleton
class ProxyFile:
    def __init__(self, path: str = None):
        self._default_proxy_file = join(expanduser('~'), '.telegram', 'proxy.json')
        self._proxy_file = self._get_proxy_file(path)

    def _get_proxy_file(self, path: str = None) -> str:
        if isinstance(path, str) and isfile(path):
            return path
        elif isfile(self._default_proxy_file):
            return self._default_proxy_file
        print(f"[red]Proxy configuration file not found")

    def get_config(self) -> dict:
        if isfile(self._proxy_file):
            config = File.read_json(self._proxy_file)

            for key in ['login', 'password', 'ip', 'port']:
                if not config.get(key, None):
                    print(f"[red]|WARNING| Empty parameter {key} in proxy.json file")
                    return {}

            proxy = Proxy(login=config['login'], password=config['password'], ip=config['ip'], port=config['port'])
            return proxy.get_param()

        return {}
