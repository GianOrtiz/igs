import sys
from PyQt5.QtWidgets import QApplication
from ui.main_window import InteractiveGraphicalSystem
from app.display_file import DisplayFile
from app.viewport import Viewport
from app.window import Window
from app.graphic.line import Line

def main():
    display_file = DisplayFile()
    window = Window(400, 0, 1000, 0, display_file)
    viewport = Viewport(window, 360, 0, 180, 0)

    app = QApplication(sys.argv)
    igs = InteractiveGraphicalSystem(viewport)
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
