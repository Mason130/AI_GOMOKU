"""
Buttons on UI
"""
from PyQt5 import QtCore
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *


class Button(QLabel):
    click_signal = pyqtSignal()
    need_emit = False

    def __init__(self, image_path, parent=None):
        super(Button, self).__init__(parent)
        self.image_0 = QPixmap(image_path[0])
        self.image_1 = QPixmap(image_path[1])
        self.image_2 = QPixmap(image_path[2])
        self.resize(self.image_0.size())
        self.setPixmap(self.image_0)
        self.setMask(self.image_1.mask())

    # press button
    def mousePressEvent(self, event):
        if event.buttons() == QtCore.Qt.LeftButton:
            self.need_emit = True
            self.setPixmap(self.image_2)

    # release button
    def mouseReleaseEvent(self, event):
        if self.need_emit:
            self.need_emit = False
            self.setPixmap(self.image_1)
            self.click_signal.emit()
