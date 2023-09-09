from .graphic.descriptor_object import DescriptorOBJ
from .graphic.object import Object

class DisplayFile:
    def __init__(self):
        self.__objects = []
    
    def objects(self) -> list[Object]:
        return self.__objects

    def add_object(self, obj):
        self.__objects.append(obj)
    
    def remove_object(self, obj):
        self.__objects.remove(obj)

    def clear_objects(self):
        self.__objects = []

    def export(self, filename: str):
        file_content = ''
        for obj in display_file.objects():
            file_content += DescriptorOBJ.export_to_OBJ(obj)
        
        with open(filename, 'w+') as f:
            f.write(file_content)

    def import_file(self, filename: str): 
        graphical_objects = DescriptorOBJ.parse(filename)
        self.clear_objects()
        for obj in graphical_objects:
            self.add_object(obj)