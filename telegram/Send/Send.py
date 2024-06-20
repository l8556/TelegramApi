# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC

class Send(ABC):

    @abstractmethod
    def send(self, *args, **kwargs) -> None: ...
