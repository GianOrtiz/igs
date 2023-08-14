class DisplayFile:
    def __init__(self):
        self.__objects = []
    
    def objects(self):
        return self.__objects

    def add_object(self, obj):
        self.__objects.insert(obj)
    
    def remove_object(self, obj):
        self.__objects.remove(obj)
