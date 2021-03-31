import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import numpy as np
import time


class ColorButton(QtWidgets.QPushButton):
    def __init__(self, parent, color):
        super().__init__(parent)
        self.active = False
        self.setFixedSize(QtCore.QSize(24, 24))
        self.set_color(color)
        # self.pressed.connect(self.showColorPicker)

    def set_active(self, value):
        self.active = value
        self.update_style()

    def set_color(self, color):
        self.color = color
        self.parent().active_color = self.color
        self.update_style()

    def update_style(self):
        color = f'background-color: {self.color.name()}'
        if self.color.red() < 128 and self.color.green() < 128:
            border_color = '#FFFFFF'
        else:
            border_color = '#000000'
        border = 'border: ' + (f'2px dashed {border_color}' if self.active else '0px')
        self.setStyleSheet('; '.join([color, border]))

    def showColorPicker(self):
        dialog = QtWidgets.QColorDialog(self)
        dialog.setCurrentColor(self.color)
        if dialog.exec_():
            self.set_color(dialog.currentColor())

    def mousePressEvent(self, QMouseEvent):
        if QMouseEvent.button() == Qt.LeftButton:
            self.parent().set_active_color(self)
        elif QMouseEvent.button() == Qt.RightButton:
            self.showColorPicker()


class Palette(QtWidgets.QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.layout = QtWidgets.QHBoxLayout(self)
        colors = [
            QtGui.QColor(255, 255, 255),
            QtGui.QColor(0, 0, 0),
            QtGui.QColor(237, 190, 164),
            QtGui.QColor(190, 237, 164),
            QtGui.QColor(164, 190, 237),
        ]
        colors[1] = QtGui.QColor(0, 0, 0)
        self.color_buttons = [ColorButton(self, color) for color in colors]
        self.color_buttons[0].set_active(True)
        self.active_color = self.color_buttons[0].color
        for button in self.color_buttons:
            self.layout.addWidget(button)

    def set_active_color(self, active_widget):
        for widget in self.color_buttons:
            widget.set_active(widget == active_widget)
        self.active_color = active_widget.color

    def get_active_color_widget(self):
        return [x for x in self.color_buttons if x.active][0]

        