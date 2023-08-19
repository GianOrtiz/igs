from PyQt5.QtWidgets import QWidget
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

class DrawingWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.__painter = QPainter(self)
        self.__lines = []

    def paintEvent(self, event):
        self.__painter.end()
        self.__painter = QPainter(self)
        self.__painter.fillRect(self.rect(), Qt.white)
        
        pen = QPen(Qt.black)
        self.__painter.setPen(pen)

        for line in self.__lines:
            x1, y1, x2, y2 = line
            self.__painter.drawLine(x1, y1, x2, y2)

    def paint(self, line):
        self.__lines.append(line)
        self.update()
