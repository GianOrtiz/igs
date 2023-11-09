from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from app.graphic.object import ObjectType
from app.graphic.line import Line, LineClippingAlgorithm
from app.graphic.point import Point
from app.graphic.object3d import Object3D, Segment
from app.graphic.point3d import Point3D
from app.graphic.wireframe import Wireframe
from app.graphic.curve import BSplineForwardDifferencesCurve, BezierCurve
from app.graphic.surface import BezierSurface

class AddObjectWindow(widgets.QMainWindow):
    def __init__(self, viewport, redraw_canvas):
        super().__init__()
        self.__viewport = viewport
        self.__select_object_type = ObjectType.POINT
        self.__redraw_canvas = redraw_canvas
        self.__should_fill_wireframe = False
        self.__curve_type = 'Bezier'
        self.__line_clipping_algorithm = LineClippingAlgorithm.LIANG_BARSKY

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
        self.__radio_button_surface = widgets.QRadioButton('Superfície Bicúbica')

        layout.addWidget(select_object_label)
        layout.addWidget(self.__radio_button_point)
        layout.addWidget(self.__radio_button_line)
        layout.addWidget(self.__radio_button_wireframe)
        layout.addWidget(self.__radio_button_curve)
        layout.addWidget(self.__radio_button_surface)

        self.__radio_button_point.toggled.connect(self.on_clicked_point)
        self.__radio_button_line.toggled.connect(self.on_clicked_line)
        self.__radio_button_wireframe.toggled.connect(self.on_clicked_wireframe)
        self.__radio_button_curve.toggled.connect(self.on_clicked_curve)
        self.__radio_button_surface.toggled.connect(self.on_clicked_surface)

        color_label = widgets.QLabel('Which color to use? (Write hexadecimal as in #000000, black will be used as default)')
        self.__color_input = widgets.QLineEdit(self)

        insert_coordinates_label = widgets.QLabel('Insira os pontos do objeto (No caso de superfícies bicubicas, utilizar 16 pontos)')
        self.__coordinates_input = widgets.QLineEdit(self)
        self.__coordinates_input.setPlaceholderText('Coordenadas em pares de segmento de pontos ((0,0,0),(1,1,1)),((10,10,10),(20,20,20))')

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
    
    def on_clicked_surface(self):
        self.__select_object_type = ObjectType.CURVE
        self.__curve_type = 'Surface'
        self.clear_input_area()

    def on_clicked_line(self):
        self.__select_object_type = ObjectType.LINE
        self.clear_input_area()

        select_line_clipping = widgets.QLabel('Which kind of clipping algorithm you want to use?')
        self.__radio_button_liang_barsky = widgets.QRadioButton('Liang Barsky')
        self.__radio_button_liang_barsky.toggle()
        self.__radio_button_cohen_sutherland = widgets.QRadioButton('Cohen Sutherland')
        
        self.input_layout.addWidget(select_line_clipping)
        self.input_layout.addWidget(self.__radio_button_liang_barsky)
        self.input_layout.addWidget(self.__radio_button_cohen_sutherland)
        
        self.__radio_button_liang_barsky.toggled.connect(self.on_clicked_liang_barsky)
        self.__radio_button_cohen_sutherland.toggled.connect(self.on_clicked_cohen_sutherland)

    def on_clicked_liang_barsky(self):
        self.__line_clipping_algorithm = LineClippingAlgorithm.LIANG_BARSKY
    
    def on_clicked_cohen_sutherland(self):
        self.__line_clipping_algorithm = LineClippingAlgorithm.COHEN_SUTHERLAND

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
            start_point = Point3D(coordinates[0][0], coordinates[0][1], coordinates[0][2])
            end_point = Point3D(coordinates[1][0], coordinates[1][1], coordinates[1][2])
            segment = Segment(start_point, end_point)
            self.__viewport.window().add_object(Object3D([segment], ObjectType.LINE, color))
        elif self.__select_object_type == ObjectType.POINT:
            if len(coordinates) != 3:
                raise "Point type object requires exactly one coordinate"
            point = Point3D(coordinates[0], coordinates[1], coordinates[2])
            segment = Segment(point, point)
            self.__viewport.window().add_object(Object3D([segment], ObjectType.POINT, color))
        elif self.__select_object_type == ObjectType.WIREFRAME:
            if len(coordinates) < 1:
                raise "Wireframe type object requires at least one coordinate"
            last_point = None
            segments: list[Segment] = []
            for coordinate in coordinates:
                point = Point3D(coordinate[0], coordinate[1], coordinate[2])
                if last_point is not None:
                    segments.append(Segment(last_point, point))
                last_point = point
            self.__viewport.window().add_object(Object3D(segments, ObjectType.WIREFRAME, color))
        elif self.__select_object_type == ObjectType.CURVE:
            if self.__curve_type == 'Surface':
                if len(coordinates) != 16:
                    raise "Surface must have 16 control points"
                self.__viewport.window().add_object(BezierSurface(coordinates, color))

            if len(coordinates) < 4:
                raise "Curve requires four coordinate points"

            if self.__curve_type == 'Bezier':
                self.__viewport.window().add_object(BezierCurve(coordinates, color))
            elif self.__curve_type == 'BSpline':
                self.__viewport.window().add_object(BSplineForwardDifferencesCurve(coordinates, color))

        self.__redraw_canvas()
        self.close()