from abc import ABC, abstractmethod
from enum import Enum
import uuid

class ObjectType(Enum):
    POINT = 1
    LINE = 2
    WIREFRAME = 3

class Object(ABC):
    def __init__(self, type):
        self.__type = type
        self.__id = uuid.uuid4().hex

    def type(self):
        return self.__type
    
    def id(self):
        return self.__id

    @abstractmethod
    def to_string(self):
        pass

    @abstractmethod
    def draw(self, draw_line, transform_coordinate):
        pass
