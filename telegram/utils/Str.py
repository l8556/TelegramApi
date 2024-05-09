# -*- coding: utf-8 -*-


def delete_last_slash(path: str) -> str:
    return path.rstrip(path[-1]) if path[-1] in ['/', '\\'] else path
