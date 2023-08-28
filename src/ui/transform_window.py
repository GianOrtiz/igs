from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from app.graphic.object import ObjectType
from app.graphic.line import Line
from app.graphic.point import Point
from app.graphic.wireframe import Wireframe

class TransformObjectWindow(widgets.QMainWindow):
    def __init__(self, viewport, redraw_canvas, obj):
        super().__init__()
        self.__viewport = viewport
        self.__redraw_canvas = redraw_canvas
        self.__object = obj
        self.__transformation = 'Scale'

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

        main_widget.setLayout(layout)

    def clear_input_area(self):
        while self.input_layout.count():
            child = self.input_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def show_scale_area(self, enabled):
        if enabled:
            self.clear_input_area()
            self.input_layout.addRow("X Factor:", widgets.QLineEdit())
            self.input_layout.addRow("Y Factor:", widgets.QLineEdit())

    def show_rotate_area(self, enabled):
        if enabled:
            self.clear_input_area()
            self.input_layout.addRow("Angle:", widgets.QLineEdit())

            rotate_type_layout = widgets.QHBoxLayout()
            self.center_world_radio = widgets.QRadioButton("Rotate from center of world")
            self.center_object_radio = widgets.QRadioButton("Rotate from center of object")
            self.point_radio = widgets.QRadioButton("Rotate from a point")
            rotate_type_layout.addWidget(self.center_world_radio)
            rotate_type_layout.addWidget(self.center_object_radio)
            rotate_type_layout.addWidget(self.point_radio)
            self.input_layout.addRow("Rotation Type:", rotate_type_layout)

            self.point_area = widgets.QWidget()
            self.point_layout = widgets.QFormLayout()
            self.point_area.setLayout(self.point_layout)
            self.input_layout.addRow("Point X:", widgets.QLineEdit())
            self.input_layout.addRow("Point Y:", widgets.QLineEdit())

    def show_translate_area(self, enabled):
        if enabled:
            self.clear_input_area()
            self.input_layout.addRow("X Translate:", widgets.QLineEdit())
            self.input_layout.addRow("Y Translate:", widgets.QLineEdit())
