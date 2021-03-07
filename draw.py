import sys
from PyQt5 import QtCore, QtGui, QtWidgets, uic
from PyQt5.QtCore import Qt


class MainWindow(QtWidgets.QMainWindow):
    WIDTH = 800
    HEIGHT = 600

    def __init__(self):
        super().__init__()
        self.label = QtWidgets.QLabel()
        canvas = QtGui.QPixmap(self.WIDTH, self.HEIGHT)
        self.label.setPixmap(canvas)
        self.setCentralWidget(self.label)
        image = self.label.pixmap().toImage()
        for x in range(self.WIDTH):
            for y in range(self.HEIGHT):
                image.setPixelColor(x, y, QtGui.QColor(255, 255, 255, 255))
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))
        # for x in [0.03, 0.11, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.89, 0.97]:
            # for y in [0.03, 0.11, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.89, 0.97]:
                # self.draw_point(int(self.WIDTH*x), int(self.HEIGHT*y), 10, 10, 10)

    def mouseMoveEvent(self, e):
        self.draw_point(e.x(), e.y(), 10, 10, 10)
        self.update()

    def mousePressEvent(self, e):
        self.draw_point(e.x(), e.y(), 10, 10, 10)
        self.update()

    def draw_point(self, center_x, center_y, red, green, blue):
        image = self.label.pixmap().toImage()
        radius = 10
        for x in range(center_x-radius, center_x+radius):
            if not (0 <= x < self.WIDTH):
                continue
            for y in range(center_y-radius, center_y+radius):
                if not (0 <= y < self.HEIGHT):
                    continue
                distance = ((x-center_x)**2 + (y-center_y)**2) ** 0.5
                if distance > radius:
                    continue
                old_color = image.pixelColor(x, y)
                # brush parameters
                max_strength_multiplier = 0.5
                inner_boundary = 0.5  # (center_y / self.HEIGHT)  # 0.5 is OK
                steepness = 0.9  # (center_x / self.WIDTH * 2)  # 0.9 is OK
                # ----------------
                strength = 1 - (max(0, distance/radius-inner_boundary)/(1-inner_boundary)) ** steepness
                strength *= max_strength_multiplier
                if not 0 <= strength <= 1:
                    print(strength)
                new_r = int(old_color.red()*(1-strength) + red*strength)
                new_g = int(old_color.green()*(1-strength) + green*strength)
                new_b = int(old_color.blue()*(1-strength) + blue*strength)
                image.setPixelColor(x, y, QtGui.QColor(new_r, new_g, new_b))
        self.label.setPixmap(QtGui.QPixmap.fromImage(image))


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()