from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from app.graphic.object import ObjectType
from app.graphic.line import Line
from app.graphic.point import Point
from app.graphic.wireframe import Wireframe

class AddObjectWindow(widgets.QMainWindow):
    def __init__(self, viewport, redraw_canvas):
        super().__init__()
        self.__viewport = viewport
        self.__select_object_type = ObjectType.POINT
        self.__redraw_canvas = redraw_canvas

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Object")
        self.setGeometry(100, 100, 800, 600)

        main_widget = widgets.QWidget(self)
        self.setCentralWidget(main_widget)

        select_object_label = widgets.QLabel('Which object you want to create?')
        self.__radio_button_point = widgets.QRadioButton('Point')
        self.__radio_button_line = widgets.QRadioButton('Line')
        self.__radio_button_wireframe = widgets.QRadioButton('Wireframe')

        self.__radio_button_point.toggled.connect(self.on_clicked_point)
        self.__radio_button_line.toggled.connect(self.on_clicked_line)
        self.__radio_button_wireframe.toggled.connect(self.on_clicked_wireframe)

        insert_coordinates_label = widgets.QLabel('Insert object coordinates as points')
        self.__coordinates_input = widgets.QLineEdit(self)

        self.__submit_button = widgets.QPushButton('Add')
        self.__submit_button.clicked.connect(self.__add_object)


        layout = widgets.QVBoxLayout()
        layout.addWidget(select_object_label)
        layout.addWidget(self.__radio_button_point)
        layout.addWidget(self.__radio_button_line)
        layout.addWidget(self.__radio_button_wireframe)
        layout.addWidget(insert_coordinates_label)
        layout.addWidget(self.__coordinates_input)
        layout.addWidget(self.__submit_button)

        main_widget.setLayout(layout)

    def on_clicked_point(self):
        self.__select_object_type = ObjectType.POINT

    def on_clicked_line(self):
        self.__select_object_type = ObjectType.LINE

    def on_clicked_wireframe(self):
        self.__select_object_type = ObjectType.WIREFRAME

    def __add_object(self):
        coordinates = list(eval(self.__coordinates_input.text()))
        if self.__select_object_type == ObjectType.LINE:
            if len(coordinates) != 2:
                raise "Line type object requires exactly two coordinates"
            self.__viewport.display_file().add_object(Line(coordinates[0], coordinates[1]))
        elif self.__select_object_type == ObjectType.POINT:
            if len(coordinates) != 2:
                raise "Point type object requires exactly one coordinate"
            self.__viewport.display_file().add_object(Point(coordinates[0], coordinates[1]))
        elif self.__select_object_type == ObjectType.WIREFRAME:
            if len(coordinates) < 1:
                raise "Wireframe type object requires at least one coordinate"
            self.__viewport.display_file().add_object(Wireframe(coordinates))

        self.__redraw_canvas()
        self.close()