from abc import ABC
from enum import Enum

class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

class Object(ABC):
    def __init__(self, type):
        self.__type = type

    def type(self):
        return self.__type
