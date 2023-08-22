import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import InteractiveGraphicalSystem
from app.display_file import DisplayFile
from app.viewport import Viewport
from app.window import Window
from app.graphic.line import Line

APP_HEIGHT = 620
APP_WIDTH = 980
APP_PADDING = 16

def main():
    display_file = DisplayFile()
    window = Window(1920, 0, 1080, 0, display_file)
    viewport = Viewport(window, 556, 0, 588, 0)

    app = QApplication(sys.argv)
    igs = InteractiveGraphicalSystem(viewport, APP_WIDTH, APP_HEIGHT)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
