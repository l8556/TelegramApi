# -*- coding: utf-8 -*-
import os

from telegram.utils import Str

from shutil import rmtree
from zipfile import ZipFile



class File:
    EXCEPTIONS = ['.DS_Store']

    @staticmethod
    def compress(path: str, archive_path: str = None, delete: bool = False, compress_type: int = 8) -> None:
        """
        :param compress_type: ZIP_STORED = 0, ZIP_DEFLATED = 8, ZIP_BZIP2 = 12, ZIP_LZMA = 14
        :param path: Path to compression files.
        :param archive_path: Path to the archive file.
        :param delete:  Deleting files after compression.
        """
        _name = os.path.basename(Str.delete_last_slash(path))
        _archive_path = archive_path or join(os.path.dirname(path) if os.path.isfile(path) else path, f"{_name}.zip")

        if not os.path.exists(path):
            return print(f'[bold red]|COMPRESS WARNING| Path for compression does not exist: {path}')

        os.makedirs(os.path.dirname(_archive_path), exist_ok=True)

        with ZipFile(_archive_path, 'w') as _zip:
            if os.path.isdir(path):
                exceptions = File.EXCEPTIONS + [f"{os.path.basename(_archive_path)}"]

                for file in File.get_paths(path):
                    if os.path.basename(file) not in exceptions:
                        _zip.write(file, os.path.relpath(file, path), compress_type=compress_type)

                if delete:
                    _archive_name = os.path.basename(_archive_path)
                    File.delete([join(path, obj) for obj in os.listdir(path) if obj != _archive_name], stdout=False)

            else:
                print(f'[green]|INFO| Compressing file: {path}')
                _zip.write(path, _name, compress_type=compress_type)
                File.delete(path, stdout=False) if delete else ...

        if os.path.exists(_archive_path) and os.path.getsize(_archive_path) != 0:
            return print(f"[green]|INFO| Success compressed: {_archive_path}")

        print(f"[WARNING] Archive not exists: {_archive_path}")

    @staticmethod
    def delete(path: "str | tuple | list", stdout: bool = False, stderr: bool = False) -> None:
        if not path:
            return print(f"[red]|DELETE ERROR| Path should be string, tuple or list not {path}") if stderr else None

        for _path in [path] if isinstance(path, str) else path:
            object_path = _path.rstrip("*")
            if not os.path.exists(object_path):
                print(f"[bold red]|DELETE WARNING| File not exist: {object_path}") if stderr else ...
                continue

            if isdir(object_path):
                rmtree(_path, ignore_errors=True)
            else:
                os.remove(object_path)

            if stderr and os.path.exists(object_path):
                print(f"[bold red]|DELETE WARNING| Is not deleted: {_path}")
            else:
                print(f'[green]|INFO| Deleted: {_path}') if stdout else ...

    @staticmethod
    def get_paths(dir_path: str) -> list:
        return [os.path.join(root, filename) for root, _, files in os.walk(dir_path) for filename in files]
