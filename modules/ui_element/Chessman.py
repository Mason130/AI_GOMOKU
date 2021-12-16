"""
Chessman on UI
"""
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from modules.ui_element.Auxiliary import *


class Chessman(QLabel):
    def __init__(self, image_path, parent=None):
        super(Chessman, self).__init__(parent)
        self.color = image_path.split(".")[-2][-5:]
        self.image = QPixmap(image_path)
        self.setFixedSize(self.image.size())
        self.setPixmap(self.image)

    # move chessman
    def move(self, point):
        x, y = pixel2chess(point)
        x = 30 * x + 50 - self.image.width() / 2
        y = 30 * y + 50 - self.image.height() / 2
        super().move(x, y)
