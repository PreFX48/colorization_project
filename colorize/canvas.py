from collections import deque
from itertools import cycle
import sys
import time

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import qimage2ndarray
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


TIP_RECT_SIZE = 6


class Canvas(QtWidgets.QLabel):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tips = {}
        self.selections = []
        self.current_selection = []
        black_image = qimage2ndarray.array2qimage(np.zeros(shape=(256, 256, 3)))
        self.original_pixmap = QtGui.QPixmap(black_image)
        self.fullsize_pixmap = self.original_pixmap.copy()
        self.updateScaledPixmap()
        self.prev_x = None
        self.prev_y = None
        self.prev_event_start_time = None
        self.prev_event_end_time = None
        self.brush_size = 20
        self.brush_opacity = 50
        self.brush_hardness = 50

    def reload_pixmap(self, pixmap):
        if not isinstance(pixmap, QtGui.QPixmap):
            pixmap = QtGui.QPixmap(pixmap)
        self.original_pixmap = pixmap.copy()
        self.fullsize_pixmap = pixmap.copy()
        self.tips = {}
        self.selections = []
        self.current_selection = []
        self.updateScaledPixmap()

    def get_image_coords(self, event):
        x, y = event.x(), event.y()
        original_size = self.fullsize_pixmap.size()
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

    def get_target_color(self):
        return self.parent().parent().palette.active_color

    def updateScaledPixmap(self):
        image = self.fullsize_pixmap.toImage()
        WIDTH = image.size().width()
        HEIGHT = image.size().height()

        # Displaying hints
        for (center_x, center_y), color in self.tips.items():
            for x in range(max(0, center_x-TIP_RECT_SIZE), min(WIDTH, center_x+TIP_RECT_SIZE+1)):
                for y in range(max(0, center_y-TIP_RECT_SIZE), min(HEIGHT, center_y+TIP_RECT_SIZE+1)):
                    if x == center_x-TIP_RECT_SIZE or x == center_x+TIP_RECT_SIZE or y == center_y-TIP_RECT_SIZE or y == center_y+TIP_RECT_SIZE:
                        image.setPixelColor(x, y, QtGui.QColor(0, 0, 0))
                    else:
                        image.setPixelColor(x, y, color)

        pixmap = QtGui.QPixmap.fromImage(image)
        # Displaying selections
        selection_colors = sorted([
            (red, green, blue)
            for red in [0, 128, 255]
            for green in [0, 128, 255]
            for blue in [0, 128, 255]
            if not (red == 255 and green == 255 and blue == 255)
            and not (red == 0 and green == 0 and blue == 0)
        ], key=lambda color: any(channel == 128 for channel in color))  # intermediate colors go last
        SELECTION_POINT_SIZE = 12
        painter = QtGui.QPainter(pixmap)
        color_idx = 0
        for selection in self.selections:
            POLYGON_BRUSH = QtGui.QBrush(QtGui.QColor(*selection_colors[color_idx]), QtCore.Qt.BrushStyle.BDiagPattern)
            LINE_PEN = QtGui.QPen(QtGui.QColor(*selection_colors[color_idx]), 3, QtCore.Qt.PenStyle.DotLine)
            painter.setBrush(POLYGON_BRUSH)
            painter.setPen(LINE_PEN)
            painter.drawPolygon(*[QtCore.QPoint(*point) for point in selection])
            painter.setPen(QtCore.Qt.PenStyle.SolidLine)
            painter.setPen(QtGui.QColor(0, 0, 0))
            painter.setBrush(QtGui.QColor(255, 255, 255))
            for x, y in selection:
                painter.drawRect(x-SELECTION_POINT_SIZE//2, y-SELECTION_POINT_SIZE//2, SELECTION_POINT_SIZE, SELECTION_POINT_SIZE)
            color_idx = (color_idx + 1) % len(selection_colors)
        # Displaying current unfinished selection
        LINE_PEN = QtGui.QPen(QtGui.QColor(*selection_colors[color_idx]), 3, QtCore.Qt.PenStyle.DotLine)
        painter.setBrush(QtCore.Qt.BrushStyle.NoBrush)
        painter.setPen(LINE_PEN)
        for start, end in zip(self.current_selection, self.current_selection[1:]):
            painter.drawLine(QtCore.QPoint(*start), QtCore.QPoint(*end))
        painter.setPen(QtCore.Qt.PenStyle.SolidLine)
        painter.setPen(QtGui.QColor(0, 0, 0))
        painter.setBrush(QtGui.QColor(255, 255, 255))
        for x, y in self.current_selection:
            painter.drawRect(x-SELECTION_POINT_SIZE//2, y-SELECTION_POINT_SIZE//2, SELECTION_POINT_SIZE, SELECTION_POINT_SIZE)
        painter.end()

        self.scaled_pixmap = pixmap.scaled(self.size(), QtCore.Qt.KeepAspectRatio, QtCore.Qt.SmoothTransformation)
        self.setPixmap(self.scaled_pixmap)

    def mouseMoveEvent(self, e):
        event_time = time.time()
        if self.prev_event_end_time:
            print('prev_end->new_start: {:.2f} msec'.format((event_time-self.prev_event_end_time)*1000))
        x, y = self.get_image_coords(e)
        if x is None:
            return
        if self.prev_x is None:
            distance = None
        else:
            distance = ((self.prev_x - x)**2 + (self.prev_y - y)**2) ** 0.5
        if distance is not None:
            print('Move distance: {:.1f}'.format(distance))
        if self.edit_mode in ('brush', 'eraser'):
            THRESHOLD = self.brush_size / 2
            if distance is not None and distance >= THRESHOLD:
                intermediate_points = np.linspace([self.prev_x, self.prev_y], [x, y], int(distance / THRESHOLD)+2).tolist()[1:-1]
                for inter_x, inter_y in intermediate_points:
                    self.draw_point(int(inter_x), int(inter_y), erase=(self.edit_mode == 'eraser'))
            self.draw_point(x, y, erase=(self.edit_mode == 'eraser'))

        self.prev_x = x
        self.prev_y = y
        self.update()
        event_end_time = time.time()
        print('start->end: {:.2f} msec'.format((event_end_time-event_time)*1000))
        self.prev_event_start_time = event_time
        self.prev_event_end_time = event_end_time

    def mousePressEvent(self, e):
        x, y = self.get_image_coords(e)
        if x is None:
            return
        self.apply_edit_mode(x, y, e)
        self.prev_x = x
        self.prev_y = y
        self.update()

    def mouseReleaseEvent(self, e):
        self.prev_x = None
        self.prev_y = None

    def resizeEvent(self, e):
        self.updateScaledPixmap()
        self.update()

    def apply_edit_mode(self, x, y, event):
        if self.edit_mode == 'brush':
            self.draw_point(x, y)
        elif self.edit_mode == 'colorpicker':
            self.pick_color(x, y)
        elif self.edit_mode == 'eraser':
            self.draw_point(x, y, erase=True)
        elif self.edit_mode == 'tip':
            self.switch_tip(x, y)
        elif self.edit_mode == 'fill':
            self.fill(x, y)
        elif self.edit_mode == 'select':
            self.add_selection(x, y, is_right_button=(event.button() == Qt.RightButton))
        else:
            raise RuntimeError('Unknown edit_mode: {}'.format(self.edit_mode))

    def switch_tip(self, center_x, center_y):
        intersecting_tips = [
            (x, y) for (x, y) in self.tips
            if (x - TIP_RECT_SIZE <= center_x <= x + TIP_RECT_SIZE) and (y - TIP_RECT_SIZE <= center_y <= y + TIP_RECT_SIZE)
        ]
        if intersecting_tips:
            for tip in intersecting_tips:
                del self.tips[tip]
        else:
            self.tips[(center_x, center_y)] = self.get_target_color()
        self.updateScaledPixmap()

    def pick_color(self, x, y):
        image = self.fullsize_pixmap.toImage()
        new_color = image.pixelColor(x, y)
        self.parent().parent().palette.get_active_color_widget().set_color(new_color)

    def draw_point(self, center_x, center_y, erase=False):
        if not erase:
            target_color = self.get_target_color()
        image = self.fullsize_pixmap.toImage()
        WIDTH = image.size().width()
        HEIGHT = image.size().height()
        radius = self.brush_size
        for x in range(center_x-radius, center_x+radius):
            if not (0 <= x < WIDTH):
                continue
            for y in range(center_y-radius, center_y+radius):
                if not (0 <= y < HEIGHT):
                    continue
                if erase:
                    target_color = self.original_pixmap.toImage().pixelColor(x, y)
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
                new_r = int(old_color.red()*(1-strength) + target_color.red()*strength)
                new_g = int(old_color.green()*(1-strength) + target_color.green()*strength)
                new_b = int(old_color.blue()*(1-strength) + target_color.blue()*strength)
                image.setPixelColor(x, y, QtGui.QColor(new_r, new_g, new_b))
        self.fullsize_pixmap = QtGui.QPixmap.fromImage(image)
        self.updateScaledPixmap()

    def fill(self, x, y):
        image = self.fullsize_pixmap.toImage()
        w, h = image.width(), image.height()
        target_color = self.get_target_color()
        start_point_color = image.pixelColor(x, y)

        have_seen = set()
        queue = deque([(x, y)])

        def get_cardinal_points(have_seen, center_pos):
            points = []
            cx, cy = center_pos
            for x, y in [(1, 0), (0, 1), (-1, 0), (0, -1)]:
                xx, yy = cx + x, cy + y
                if (xx >= 0 and xx < w and yy >= 0 and yy < h and (xx, yy) not in have_seen):
                    points.append((xx, yy))
                    have_seen.add((xx, yy))
            return points

        def is_point_good(x, y):
            point_color = image.pixelColor(x, y)
            TOLERANCE = 10
            if abs(point_color.red() - start_point_color.red()) > TOLERANCE:
                return False
            if abs(point_color.green() - start_point_color.green()) > TOLERANCE:
                return False
            if abs(point_color.blue() - start_point_color.blue()) > TOLERANCE:
                return False
            return True

        while queue:
            x, y = queue.popleft()
            if is_point_good(x, y):
                image.setPixelColor(x, y, target_color)
                # Prepend to the queue
                queue.extend(get_cardinal_points(have_seen, (x, y)))

        self.fullsize_pixmap = QtGui.QPixmap.fromImage(image)
        self.updateScaledPixmap()

    def add_selection(self, x, y, is_right_button):
        if is_right_button and not self.current_selection:
            point = Point(x, y)
            for selection in list(self.selections):
                polygon = Polygon(selection)
                if polygon.contains(point):
                    self.selections.remove(selection)
        else:
            self.current_selection.append((x, y))
            if is_right_button and len(self.current_selection) >= 3:
                self.selections.append(tuple(self.current_selection))
                self.current_selection = []
        self.updateScaledPixmap()
