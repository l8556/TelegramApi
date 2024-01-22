# -*- coding: utf-8 -*-

class Proxy:
    def __init__(self, login: str, password: str, ip: str, port: str):
        self.login = login
        self.password = password
        self.ip = ip
        self.port = port

    def get_param(self) -> dict:
        proxy = f"http://{self.login}:{self.password}@{self.ip}:{self.port}"
        return  {'http': proxy, 'https': proxy}
