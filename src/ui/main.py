import sys
from PyQt5.QtWidgets import QApplication
from main_window import InteractiveGraphicalSystem

def main():
    app = QApplication(sys.argv)
    igs = InteractiveGraphicalSystem()
    sys.exit(app.exec())
