from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from .add_object_window import AddObjectWindow
from .drawing import DrawingWidget

class InteractiveGraphicalSystem(widgets.QMainWindow):
    def __init__(self, viewport, width, height):
        super().__init__()
        self.__viewport = viewport
        self.__width = width
        self.__height = height

        self.initUI()

    def initUI(self):
        self.setWindowTitle("Interactive Graphical System")
        self.setGeometry(0, 0, self.__width, self.__height)

        main_widget = widgets.QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = widgets.QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Left Panel
        left_panel = widgets.QWidget(self)
        left_panel.setMaximumWidth(360)
        left_panel.setMaximumHeight(588)
        main_layout.addWidget(left_panel)

        left_layout = widgets.QVBoxLayout()
        left_panel.setLayout(left_layout)

        # List of Graphical Objects
        self.__object_list = widgets.QListWidget(self)
        self.__render_objects_list()
        left_layout.addWidget(self.__object_list)

        # Directional Buttons
        directional_buttons = widgets.QHBoxLayout()
        up_direction_button = widgets.QPushButton('Up')
        up_direction_button.clicked.connect(self.__window_move_top)
        directional_buttons.addWidget(up_direction_button)
        down_direction_button = widgets.QPushButton('Down')
        down_direction_button.clicked.connect(self.__window_move_bottom)
        directional_buttons.addWidget(down_direction_button)
        right_direction_button = widgets.QPushButton('Right')
        right_direction_button.clicked.connect(self.__window_move_right)
        directional_buttons.addWidget(right_direction_button)
        left_direction_button = widgets.QPushButton('Left')
        left_direction_button.clicked.connect(self.__window_move_left)
        directional_buttons.addWidget(left_direction_button)
        left_layout.addLayout(directional_buttons)

        # Zoom Buttons
        zoom_buttons = widgets.QHBoxLayout()
        zoom_in_button = widgets.QPushButton("Zoom In")
        zoom_in_button.clicked.connect(self.__window_zoom_in)
        zoom_out_button = widgets.QPushButton("Zoom Out")
        zoom_out_button.clicked.connect(self.__window_zoom_out)
        zoom_buttons.addWidget(zoom_in_button)
        zoom_buttons.addWidget(zoom_out_button)
        left_layout.addLayout(zoom_buttons)

        # Add Object Button
        add_object_button = widgets.QPushButton("Add Object")
        left_layout.addWidget(add_object_button)
        add_object_button.clicked.connect(self.on_add_object_clicked)

        right_panel = widgets.QWidget(self)
        main_layout.addWidget(right_panel)

        right_layout = widgets.QVBoxLayout()
        right_panel.setLayout(right_layout)

        # Viewport
        canvas_panel = widgets.QWidget(self)
        canvas_panel.setMaximumHeight(self.__viewport.y_max())
        canvas_panel.setMaximumWidth(self.__viewport.x_max())
        right_layout.addWidget(canvas_panel)
        canvas_layout = widgets.QVBoxLayout()
        canvas_panel.setLayout(canvas_layout)
        self.__drawing = DrawingWidget()
        self.__drawing.setFixedSize(self.__viewport.x_max(), self.__viewport.y_max())

        # self.canvas.setScene(self.scene)
        canvas_layout.addWidget(self.__drawing)

        self.show()

        self.redraw_canvas()

    def redraw_canvas(self):
        lines_to_draw = self.__viewport.lines_to_draw()
        for line in lines_to_draw:
            self.__drawing.paint((line[0], line[1], line[2], line[3]))

        self.__render_objects_list()

    def on_add_object_clicked(self):
        self.add_object_window = AddObjectWindow(self.__viewport, self.redraw_canvas)
        self.add_object_window.show()

    def __window_zoom_in(self):
        self.__viewport.window().zoom_in()
        self.redraw_canvas()
    
    def __window_zoom_out(self):
        self.__viewport.window().zoom_out()
        self.redraw_canvas()
    
    def __window_move_left(self):
        self.__viewport.window().move_left()
        self.redraw_canvas()
    
    def __window_move_right(self):
        self.__viewport.window().move_right()
        self.redraw_canvas()
    
    def __window_move_top(self):
        self.__viewport.window().move_top()
        self.redraw_canvas()

    def __window_move_bottom(self):
        self.__viewport.window().move_bottom()
        self.redraw_canvas()

    def __render_objects_list(self):
        objects = self.__viewport.display_file().objects()
        self.__object_list.clear()
        for obj in objects:
            self.__object_list.addItem(obj.to_string())
