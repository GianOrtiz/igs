from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from app.graphic.object import ObjectType
from app.graphic.line import Line
from app.graphic.point import Point
from app.graphic.wireframe import Wireframe
from app.graphic.curve import BSplineForwardDifferencesCurve, BezierCurve

class AddObjectWindow(widgets.QMainWindow):
    def __init__(self, viewport, redraw_canvas):
        super().__init__()
        self.__viewport = viewport
        self.__select_object_type = ObjectType.POINT
        self.__redraw_canvas = redraw_canvas
        self.__should_fill_wireframe = False

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Add Object")
        self.setGeometry(100, 100, 800, 600)

        main_widget = widgets.QWidget(self)
        self.setCentralWidget(main_widget)

        layout = widgets.QVBoxLayout()

        select_object_label = widgets.QLabel('Which object you want to create?')
        self.__radio_button_point = widgets.QRadioButton('Point')
        self.__radio_button_point.toggle()
        self.__radio_button_line = widgets.QRadioButton('Line')
        self.__radio_button_wireframe = widgets.QRadioButton('Wireframe')
        self.__radio_button_curve = widgets.QRadioButton('Curve')

        layout.addWidget(select_object_label)
        layout.addWidget(self.__radio_button_point)
        layout.addWidget(self.__radio_button_line)
        layout.addWidget(self.__radio_button_wireframe)
        layout.addWidget(self.__radio_button_curve)

        self.__radio_button_point.toggled.connect(self.on_clicked_point)
        self.__radio_button_line.toggled.connect(self.on_clicked_line)
        self.__radio_button_wireframe.toggled.connect(self.on_clicked_wireframe)
        self.__radio_button_curve.toggled.connect(self.on_clicked_curve)

        color_label = widgets.QLabel('Which color to use? (Write hexadecimal as in #000000, black will be used as default)')
        self.__color_input = widgets.QLineEdit(self)

        insert_coordinates_label = widgets.QLabel('Insert object coordinates as points')
        self.__coordinates_input = widgets.QLineEdit(self)

        self.__submit_button = widgets.QPushButton('Add')
        self.__submit_button.clicked.connect(self.__add_object)

        layout.addWidget(select_object_label)
        layout.addWidget(self.__radio_button_point)
        layout.addWidget(self.__radio_button_line)
        layout.addWidget(self.__radio_button_wireframe)
        layout.addWidget(color_label)
        layout.addWidget(self.__color_input)
        layout.addWidget(insert_coordinates_label)
        layout.addWidget(self.__coordinates_input)

        self.input_area = widgets.QWidget()
        self.input_layout = widgets.QFormLayout()
        self.input_area.setLayout(self.input_layout)
        layout.addWidget(self.input_area)

        layout.addWidget(self.__submit_button)

        main_widget.setLayout(layout)

    def on_clicked_point(self):
        self.__select_object_type = ObjectType.POINT
        self.clear_input_area()

    def on_clicked_line(self):
        self.__select_object_type = ObjectType.LINE
        self.clear_input_area()

    def clear_input_area(self):
        while self.input_layout.count():
            child = self.input_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

    def on_clicked_curve(self):
        self.__select_object_type = ObjectType.CURVE
        self.clear_input_area()

        select_curve_type = widgets.QLabel('Which kind of curve you want to use?')
        self.__radio_button_bezier = widgets.QRadioButton('Bezier')
        self.__radio_button_bezier.toggle()
        self.__radio_button_bspline_curve = widgets.QRadioButton('BSpline with Forward Differences')
        
        self.input_layout.addWidget(select_curve_type)
        self.input_layout.addWidget(self.__radio_button_bezier)
        self.input_layout.addWidget(self.__radio_button_bspline_curve)
        
        self.__radio_button_bezier.toggled.connect(self.on_clicked_bezier)
        self.__radio_button_bspline_curve.toggled.connect(self.on_clicked_bspline)

    def on_clicked_bezier(self):
        self.__curve_type = 'Bezier'

    def on_clicked_bspline(self):
        self.__curve_type = 'BSpline'        

    def on_clicked_wireframe(self):
        self.__select_object_type = ObjectType.WIREFRAME
        self.clear_input_area()

        self.should_fill_wireframe_label = widgets.QLabel("Should fill the Wireframe?")
        self.should_fill_wireframe_true = widgets.QRadioButton('True')
        self.should_fill_wireframe_false = widgets.QRadioButton('False')
        self.should_fill_wireframe_false.toggle()
        self.input_layout.addWidget(self.should_fill_wireframe_label)
        self.should_fill_wireframe_true.toggled.connect(self.on_should_fill_wireframe)
        self.should_fill_wireframe_false.toggled.connect(self.on_should_not_fill_wireframe)
        self.input_layout.addWidget(self.should_fill_wireframe_true)
        self.input_layout.addWidget(self.should_fill_wireframe_false)

    def on_should_fill_wireframe(self, enabled):
        if enabled:
            self.__should_fill_wireframe = True

    def on_should_not_fill_wireframe(self, enabled):
        if enabled:
            self.__should_fill_wireframe = False

    def __add_object(self):
        color = self.__color_input.text()
        if color == '':
            color = '#000000'
        coordinates = list(eval(self.__coordinates_input.text()))
        if self.__select_object_type == ObjectType.LINE:
            if len(coordinates) != 2:
                raise "Line type object requires exactly two coordinates"
            self.__viewport.window().add_object(Line(coordinates[0], coordinates[1], color))
        elif self.__select_object_type == ObjectType.POINT:
            if len(coordinates) != 2:
                raise "Point type object requires exactly one coordinate"
            self.__viewport.window().add_object(Point(coordinates[0], coordinates[1], color))
        elif self.__select_object_type == ObjectType.WIREFRAME:
            if len(coordinates) < 1:
                raise "Wireframe type object requires at least one coordinate"
            self.__viewport.window().add_object(Wireframe(coordinates, color, self.__should_fill_wireframe))
        elif self.__select_object_type == ObjectType.CURVE:
            if len(coordinates) < 4:
                raise "Curve requires four coordinate points"

            if self.__curve_type == 'Bezier':
                self.__viewport.window().add_object(BezierCurve(coordinates, color))
            elif self.__curve_type == 'BSpline':
                self.__viewport.window().add_object(BSplineForwardDifferencesCurve(coordinates, color))

        self.__redraw_canvas()
        self.close()