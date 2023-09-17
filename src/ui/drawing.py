from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor, QBrush
from PyQt5.QtCore import Qt

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__painter = QPainter(self)
        self.__lines = []
        self.__filled_paths = []

    def clear_lines(self):
        self.__lines = []
        self.__filled_paths = []

    def paintEvent(self, event):
        self.__painter.end()
        self.__painter = QPainter(self)
        self.__painter.fillRect(self.rect(), Qt.white)

        for line in self.__lines:
            x1, y1, x2, y2, color = line
            pen = QPen(QColor(color))
            self.__painter.setPen(pen)
            self.__painter.drawLine(int(x1), int(y1), int(x2), int(y2))
        
        for path in self.__filled_paths:
            self.__painter.fillPath(path, QBrush(Qt.SolidPattern))

    def paint_filled_path(self, path):
        self.__filled_paths.append(path)
        self.update()

    def paint(self, line):
        self.__lines.append(line)
        self.update()
