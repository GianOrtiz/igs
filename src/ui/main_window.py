from PyQt5.QtCore import Qt
import PyQt5.QtWidgets as widgets
from .add_object_window import AddObjectWindow

class InteractiveGraphicalSystem(widgets.QMainWindow):
    def __init__(self, viewport):
        super().__init__()
        self.__viewport = viewport
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Interactive Graphical System")
        self.setGeometry(100, 100, 800, 600)

        main_widget = widgets.QWidget(self)
        self.setCentralWidget(main_widget)

        main_layout = widgets.QHBoxLayout()
        main_widget.setLayout(main_layout)

        # Left Panel
        left_panel = widgets.QWidget(self)
        left_panel.setMaximumWidth(int(self.width() * 0.24))
        main_layout.addWidget(left_panel)

        left_layout = widgets.QVBoxLayout()
        left_panel.setLayout(left_layout)

        # List of Graphical Objects
        object_list = widgets.QListWidget(self)
        left_layout.addWidget(object_list)

        # Directional Buttons
        directional_buttons = widgets.QHBoxLayout()
        for direction in ['Up', 'Down', 'Left', 'Right']:
            direction_button = widgets.QPushButton(direction)
            directional_buttons.addWidget(direction_button)
        left_layout.addLayout(directional_buttons)

        # Zoom Buttons
        zoom_buttons = widgets.QHBoxLayout()
        zoom_in_button = widgets.QPushButton("Zoom In")
        zoom_out_button = widgets.QPushButton("Zoom Out")
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
        canvas_panel.setMaximumHeight(int(self.height() * 0.76))
        right_layout.addWidget(canvas_panel)
        canvas_layout = widgets.QVBoxLayout()
        canvas_panel.setLayout(canvas_layout)

        self.canvas = widgets.QGraphicsView()
        self.canvas.setFixedSize(self.__viewport.x_max(), self.__viewport.y_max())
        self.scene = widgets.QGraphicsScene()

        lines_to_draw = self.__viewport.lines_to_draw()
        for line in lines_to_draw:
            self.scene.addLine(lines_to_draw[0], lines_to_draw[1], lines_to_draw[2], lines_to_draw[3])

        self.canvas.setScene(self.scene)
        canvas_layout.addWidget(self.canvas)

        # Log Area
        log_panel = widgets.QWidget(self)
        log_panel.setMaximumHeight(int(self.height() * 0.24))
        right_layout.addWidget(log_panel)
        log_layout = widgets.QVBoxLayout()
        log_panel.setLayout(log_layout)

        log_area = widgets.QLabel("Log Area")
        log_area.setAlignment(Qt.AlignCenter)
        log_layout.addWidget(log_area)

        self.show()

    def on_add_object_clicked(self):
        self.add_object_window = AddObjectWindow(self.__viewport)
        self.add_object_window.show()
