import math

from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from app.graphic.object import ObjectType
from app.graphic.line import Line
from app.graphic.point3d import Point3D
from enum import Enum

class TransformationType(Enum):
    SCALE = 1
    ROTATE = 2
    TRANSLATE = 3

class RotationType(Enum):
    FROM_CENTER_OF_OBJECT = 1
    FROM_CENTER_OF_WORLD = 2
    FROM_POINT = 3

class TransformObjectWindow(widgets.QMainWindow):
    def __init__(self, viewport, redraw_canvas, obj):
        super().__init__()
        self.__viewport = viewport
        self.__redraw_canvas = redraw_canvas
        self.__object = obj
        self.__transformation = TransformationType.SCALE
        self.__rotation_type = RotationType.FROM_CENTER_OF_OBJECT

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Transform object")
        self.setGeometry(0, 0, 800, 600)

        main_widget = widgets.QWidget(self)
        self.setCentralWidget(main_widget)
        layout = widgets.QVBoxLayout()

        self.transformation_label = widgets.QLabel("Which transformation would you like to apply?")
        layout.addWidget(self.transformation_label)

        self.scale_radio = widgets.QRadioButton("Scale")
        self.rotate_radio = widgets.QRadioButton("Rotate")
        self.translate_radio = widgets.QRadioButton("Translate")

        self.scale_radio.toggled.connect(self.show_scale_area)
        self.rotate_radio.toggled.connect(self.show_rotate_area)
        self.translate_radio.toggled.connect(self.show_translate_area)

        layout.addWidget(self.scale_radio)
        layout.addWidget(self.rotate_radio)
        layout.addWidget(self.translate_radio)

        self.input_area = widgets.QWidget()
        self.input_layout = widgets.QFormLayout()
        self.input_area.setLayout(self.input_layout)
        layout.addWidget(self.input_area)

        self.__submit_button = widgets.QPushButton('Transform')
        self.__submit_button.clicked.connect(self.__transform)
        layout.addWidget(self.__submit_button)

        main_widget.setLayout(layout)

    def clear_input_area(self):
        while self.input_layout.count():
            child = self.input_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_scale_area(self, enabled):
        if enabled:
            self.__transformation = TransformationType.SCALE

            self.clear_input_area()
            self.__x_factor_input = widgets.QLineEdit()
            self.__y_factor_input = widgets.QLineEdit()
            self.__z_factor_input = widgets.QLineEdit()
            self.input_layout.addRow("X Factor:", self.__x_factor_input)
            self.input_layout.addRow("Y Factor:", self.__y_factor_input)
            self.input_layout.addRow("Z Factor:", self.__z_factor_input)

    def show_rotate_area(self, enabled):
        if enabled:
            self.__transformation = TransformationType.ROTATE
            self.__rotation_type = RotationType.FROM_CENTER_OF_WORLD

            self.clear_input_area()
            self.__angle_input = widgets.QLineEdit()
            self.input_layout.addRow("Angle:", self.__angle_input)

            rotate_type_layout = widgets.QHBoxLayout()
            self.center_world_radio = widgets.QRadioButton("Rotate from center of world")
            self.center_world_radio.toggled.connect(self.rotate_from_center_world)
            self.center_object_radio = widgets.QRadioButton("Rotate from center of object")
            self.center_object_radio.toggled.connect(self.rotate_from_center_object)
            self.point_radio = widgets.QRadioButton("Rotate from a point")
            self.point_radio.toggled.connect(self.rotate_from_point)
            rotate_type_layout.addWidget(self.center_world_radio)
            rotate_type_layout.addWidget(self.center_object_radio)
            rotate_type_layout.addWidget(self.point_radio)
            self.input_layout.addRow("Rotation Type:", rotate_type_layout)

            self.point_area = widgets.QWidget()
            self.point_layout = widgets.QFormLayout()
            self.point_area.setLayout(self.point_layout)
            self.__rotate_point_x_input = widgets.QLineEdit()
            self.__rotate_point_y_input = widgets.QLineEdit()
            self.__rotate_point_z_input = widgets.QLineEdit()
            self.input_layout.addRow("Point X:", self.__rotate_point_x_input)
            self.input_layout.addRow("Point Y:", self.__rotate_point_y_input)
            self.input_layout.addRow("Point Z:", self.__rotate_point_z_input)

    def rotate_from_center_world(self, enabled):
        if enabled:
            self.__rotation_type = RotationType.FROM_CENTER_OF_WORLD
    
    def rotate_from_center_object(self, enabled):
        if enabled:
            self.__rotation_type = RotationType.FROM_CENTER_OF_OBJECT

    def rotate_from_point(self, enabled):
        if enabled:
            self.__rotation_type = RotationType.FROM_POINT

    def show_translate_area(self, enabled):
        if enabled:
            self.__transformation = TransformationType.TRANSLATE

            self.clear_input_area()
            self.__x_translate_input = widgets.QLineEdit()
            self.__y_translate_input = widgets.QLineEdit()
            self.__z_translate_input = widgets.QLineEdit()
            self.input_layout.addRow("X Translate:", self.__x_translate_input)
            self.input_layout.addRow("Y Translate:", self.__y_translate_input)
            self.input_layout.addRow("Z Translate:", self.__z_translate_input)

    def degree_to_radians(self, angle):
        return angle * (math.pi / 180)

    def __transform(self):
        if self.__transformation == TransformationType.SCALE:
            self.scale()
        elif self.__transformation == TransformationType.TRANSLATE:
            self.translate()
        else:
           self.rotate()

        self.__redraw_canvas()
        self.close()

    def scale(self):
        try:
            x = int(self.__x_factor_input.text())
        except:
            x = 1
        
        try:
            y = int(self.__y_factor_input.text())
        except:
            y = 1

        try:
            z = int(self.__z_factor_input.text())
        except:
            z = 1

        self.__object.scale((x, y, z))

    def translate(self):
        try:
            x = int(self.__x_translate_input.text())
        except:
            x = 1
        
        try:
            y = int(self.__y_translate_input.text())
        except:
            y = 1

        try:
            z = int(self.__z_translate_input.text())
        except:
            z = 1

        self.__object.translate((x, y, z))

    def rotate(self):
        try:
            angle = self.degree_to_radians(int(self.__angle_input.text()))
        except:
            # Angle 0 does nothing to the graphical object as it rotates the object over nothing.
            angle = 0

        if self.__rotation_type == RotationType.FROM_CENTER_OF_OBJECT:
            self.__object.rotate_from_axis(angle, Point3D(0,0,0))
        elif self.__rotation_type == RotationType.FROM_CENTER_OF_WORLD:
            self.__object.rotate_y(angle)
        else:
            try:
                x = int(self.__rotate_point_x_input.text())
            except:
                x = 0
            
            try:
                y = int(self.__rotate_point_y_input.text())
            except:
                y = 0

            try:
                z = int(self.__rotate_point_z_input.text())
            except:
                z = 0

            self.__object.rotate_from_axis(angle, Point3D(x, y, z))