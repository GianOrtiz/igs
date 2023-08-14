from abc import ABC
from enum import Enum
import uuid

class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

class Object(ABC):
    def __init__(self, type):
        self.__type = type
        self.__id = uuid.uuid4().bytes

    def type(self):
        return self.__type
    
    def id(self):
        return self.__id
