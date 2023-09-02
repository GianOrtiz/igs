from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen, QColor
from PyQt5.QtCore import Qt

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__painter = QPainter(self)
        self.__lines = []

    def clear_lines(self):
        self.__lines = []

    def paintEvent(self, event):
        self.__painter.end()
        self.__painter = QPainter(self)
        self.__painter.fillRect(self.rect(), Qt.white)

        for line in self.__lines:
            x1, y1, x2, y2, color = line
            pen = QPen(QColor(color))
            self.__painter.setPen(pen)
            self.__painter.drawLine(int(x1), int(y1), int(x2), int(y2))

    def paint(self, line):
        self.__lines.append(line)
        self.update()
