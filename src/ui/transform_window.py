from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from app.graphic.object import ObjectType
from app.graphic.line import Line
from app.graphic.point import Point
from app.graphic.wireframe import Wireframe

class AddObjectWindow(widgets.QMainWindow):
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

        select_transformation_label = widgets.QLabel('Which transformation would you like to apply?')
        self.__radio_button_scale = widgets.QRadioButton('Scale')
        self.__radio_button_rotate = widgets.QRadioButton('Rotate')
        self.__radio_button_translade = widgets.QRadioButton('Translade')

        self.__radio_button_scale.toggled.connect(self.on_clicked_scale)
        self.__radio_button_rotate.toggled.connect(self.on_clicked_rotate)
        self.__radio_button_translade.toggled.connect(self.on_clicked_translade)

        self.__submit_button = widgets.QPushButton('Transform')
        self.__submit_button.clicked.connect(self.__submit)

        layout = widgets.QVBoxLayout()
        layout.addWidget(select_object_label)
        layout.addWidget(self.__radio_button_scale)
        layout.addWidget(self.__radio_button_rotate)
        layout.addWidget(self.__radio_button_translade)
        layout.addWidget(self.__submit_button)

        main_widget.setLayout(layout)

    def on_clicked_scale(self):
        self.__transformation = 'Scale'

    def on_clicked_rotate(self):
        self.__transformation = 'Rotate'

    def on_clicked_translade(self):
        self.__transformation = 'Translade'

    def __submit(self):


        self.__redraw_canvas()
        self.close()

# Scale should input x and y scaling factors.
# Rotate should select between "rotating from center of object", "rotating from center of world" and "rotating from point".
# If "rotating from point" is selected a point must be given as input.
# Translade should input x and y translade factors.


    # def __init__(self):
    #     super().__init__()

    #     self.setWindowTitle("Transformation App")
    #     layout = QVBoxLayout()

    #     self.transformation_label = QLabel("Which transformation would you like to apply?")
    #     layout.addWidget(self.transformation_label)

    #     self.scale_radio = QRadioButton("Scale")
    #     self.rotate_radio = QRadioButton("Rotate")
    #     self.translate_radio = QRadioButton("Translate")

    #     self.scale_radio.toggled.connect(self.show_scale_area)
    #     self.rotate_radio.toggled.connect(self.show_rotate_area)
    #     self.translate_radio.toggled.connect(self.show_translate_area)

    #     layout.addWidget(self.scale_radio)
    #     layout.addWidget(self.rotate_radio)
    #     layout.addWidget(self.translate_radio)

    #     self.input_area = QWidget()
    #     self.input_layout = QFormLayout()
    #     self.input_area.setLayout(self.input_layout)
    #     layout.addWidget(self.input_area)

    #     self.setLayout(layout)

    # def clear_input_area(self):
    #     while self.input_layout.count():
    #         child = self.input_layout.takeAt(0)
    #         if child.widget():
    #             child.widget().deleteLater()

    # def show_scale_area(self, enabled):
    #     if enabled:
    #         self.clear_input_area()
    #         self.input_layout.addRow("X Factor:", QLineEdit())
    #         self.input_layout.addRow("Y Factor:", QLineEdit())

    # def show_rotate_area(self, enabled):
    #     if enabled:
    #         self.clear_input_area()
    #         self.input_layout.addRow("Angle:", QLineEdit())

    #         rotate_type_layout = QHBoxLayout()
    #         self.center_world_radio = QRadioButton("Rotate from center of world")
    #         self.center_object_radio = QRadioButton("Rotate from center of object")
    #         self.point_radio = QRadioButton("Rotate from a point")
    #         rotate_type_layout.addWidget(self.center_world_radio)
    #         rotate_type_layout.addWidget(self.center_object_radio)
    #         rotate_type_layout.addWidget(self.point_radio)
    #         self.input_layout.addRow("Rotation Type:", rotate_type_layout)

    #         self.point_area = QWidget()
    #         self.point_layout = QFormLayout()
    #         self.point_area.setLayout(self.point_layout)
    #         self.input_layout.addRow("Point X:", QLineEdit())
    #         self.input_layout.addRow("Point Y:", QLineEdit())

    # def show_translate_area(self, enabled):
    #     if enabled:
    #         self.clear_input_area()
    #         self.input_layout.addRow("X Translate:", QLineEdit())
    #         self.input_layout.addRow("Y Translate:", QLineEdit())
