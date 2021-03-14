import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import numpy as np
import time


class Canvas(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.original_pixmap = QtGui.QPixmap('/Users/v-sopov/projects/hse/colorization/sample_image.png')
        self.updateScaledPixmap()
        self.prev_x = None
        self.prev_y = None
        self.prev_event_start_time = None
        self.prev_event_end_time = None
        self.brush_size = 20
        self.brush_opacity = 50
        self.brush_hardness = 50

    def getImageCoords(self, event):
        x, y = event.x(), event.y()
        original_size = self.original_pixmap.size()
        original_width = original_size.width()
        original_height = original_size.height()
        scaled_size = self.scaled_pixmap.size()
        scaled_width = scaled_size.width()
        scaled_height = scaled_size.height()
        scaled_x_offset = (self.size().width() - scaled_width) // 2
        scaled_y_offset = (self.size().height() - scaled_height) // 2
        x -= scaled_x_offset
        y -= scaled_y_offset
        if not (0 <= x < scaled_width):
            return None, None
        if not (0 <= y < scaled_height):
            return None, None
        x = int(x / scaled_width * original_width)
        y = int(y / scaled_height * original_height)
        return x, y

    def updateScaledPixmap(self):
        # TODO: fix disappearance of all drawings after window resize
        self.scaled_pixmap = self.original_pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.scaled_pixmap)

    def mouseMoveEvent(self, e):
        event_time = time.time()
        if self.prev_event_end_time:
            print('prev_end->new_start: {:.2f} msec'.format((event_time-self.prev_event_end_time)*1000))
        x, y = self.getImageCoords(e)
        if x is None:
            return
        if self.prev_x is None:
            distance = None
        else:
            distance = ((self.prev_x - x)**2 + (self.prev_y - y)**2) ** 0.5
        if distance is not None:
            print('Move distance: {:.1f}'.format(distance))
        THRESHOLD = 7.0
        if distance is not None and distance >= THRESHOLD:
            intermediate_points = np.linspace([self.prev_x, self.prev_y], [x, y], int(distance / THRESHOLD)+2).tolist()[1:-1]
            for inter_x, inter_y in intermediate_points:
                self.draw_point(int(inter_x), int(inter_y), 10, 10, 10)
        self.draw_point(x, y, 10, 10, 10)

        self.prev_x = x
        self.prev_y = y
        self.update()
        event_end_time = time.time()
        print('start->end: {:.2f} msec'.format((event_end_time-event_time)*1000))
        self.prev_event_start_time = event_time
        self.prev_event_end_time = event_end_time

    def mousePressEvent(self, e):
        x, y = self.getImageCoords(e)
        if x is None:
            return
        self.draw_point(x, y, 10, 10, 10)
        self.prev_x = x
        self.prev_y = y
        self.update()

    def mouseReleaseEvent(self, e):
        self.prev_x = None
        self.prev_y = None

    def resizeEvent(self, e):
        self.updateScaledPixmap()
        self.update()

    def draw_point(self, center_x, center_y, red, green, blue):
        image = self.original_pixmap.toImage()
        WIDTH = image.size().width()
        HEIGHT = image.size().height()
        radius = self.brush_size
        for x in range(center_x-radius, center_x+radius):
            if not (0 <= x < WIDTH):
                continue
            for y in range(center_y-radius, center_y+radius):
                if not (0 <= y < HEIGHT):
                    continue
                distance = ((x-center_x)**2 + (y-center_y)**2) ** 0.5
                if distance > radius:
                    continue
                old_color = image.pixelColor(x, y)
                # brush parameters
                # max_strength_multiplier = 0.5
                max_strength_multiplier = self.brush_opacity / 100
                # inner_boundary = 0.5  # (center_y / HEIGHT)  # 0.5 is OK
                inner_boundary = min(0.99, max(0.01, self.brush_hardness / 100))
                # steepness = 0.9  # (center_x / WIDTH * 2)  # 0.9 is OK
                steepness = min(0.99, max(0.01, self.brush_hardness / 100))  # 0.9 is OK
                # ----------------
                strength = 1 - (max(0, distance/radius-inner_boundary)/(1-inner_boundary)) ** steepness
                strength *= max_strength_multiplier
                if not 0 <= strength <= 1:
                    print(strength)
                new_r = int(old_color.red()*(1-strength) + red*strength)
                new_g = int(old_color.green()*(1-strength) + green*strength)
                new_b = int(old_color.blue()*(1-strength) + blue*strength)
                image.setPixelColor(x, y, QtGui.QColor(new_r, new_g, new_b))
        self.original_pixmap = QtGui.QPixmap.fromImage(image)
        self.updateScaledPixmap()


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()
        self.canvas = Canvas()
        w = QtWidgets.QWidget()
        l = QtWidgets.QVBoxLayout()
        w.setLayout(l)
        l.addWidget(self.canvas)
        self.setWindowTitle('Colorize')

        # palette = QtWidgets.QHBoxLayout()
        # self.add_palette_buttons(palette)
        # l.addLayout(palette)

        self.setCentralWidget(w)


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()