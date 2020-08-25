# albus.model
from abc import ABC, abstractmethod
from typing import Any

from albus.exceptions import AlbusError


class Data(ABC):

    @abstractmethod
    def _store_value(self, value: Any, key: str = None):
        raise NotImplementedError()

    @abstractmethod
    def _load_value(self, key: str = None):
        raise NotImplementedError()


class Model(Data):

    def __init__(self):
        self.__data = {}

    def _store_value(self, value: Any, key: str = None):
        self.__data[key] = value

    def _load_value(self, key: str = None):
        return self.__data[key]


class FieldDescriptor(Data):

    def __set_name__(self, owner, name):
        if not issubclass(owner, Model):
            raise AlbusError(
                "Bad container",
                detail="Fields can only be bound to models.",
            )
        self.owner = owner
        self.name = name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        return self.owner._load_value(key=self.name)

    def __set__(self, obj, value):
        obj._store_value(value, key=self.name)


class Field(FieldDescriptor):

    pass
