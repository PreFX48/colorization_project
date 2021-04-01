from functools import partial
import os
import sys

import cv2
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import qimage2ndarray
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import torch

import form
from dl.colorizator import MangaColorizator
from dl.utils.utils import resize_pad 


EDIT_MODES = ['brush', 'colorpicker', 'eraser', 'fill', 'tip', 'select']


class ColorizerWorker(QtCore.QObject):
    finished = QtCore.pyqtSignal()
    progress = QtCore.pyqtSignal(str)

    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window

    def prepare_hints_mask(self, img_arr):
        size = 576
        if (img_arr.shape[0] < img_arr.shape[1]):
            ratio = img_arr.shape[0] / (size * 1.5)
            height = int(size*1.5)
            width = int(np.ceil(img_arr.shape[1] / ratio))
            padding = ((0, 0), (0, 32-width%32), (0, 0))
        else:
            ratio = img_arr.shape[1] / size
            height = int(np.ceil(img_arr.shape[0] / ratio))
            width = size
            padding = ((0, 32-height%32), (0, 0), (0, 0))
        
        height_ratio = height / img_arr.shape[0]
        width_ratio = width / img_arr.shape[1]

        color_map = np.full((height, width, 3), 0.5)
        mask = np.zeros(shape=(height, width, 1))
        HINT_RADIUS = 0
        for (unscaled_x, unscaled_y), color in self.window.raw_image.tips.items():
            x = int(unscaled_x * width_ratio)
            y = int(unscaled_y * height_ratio)
            for x_ in range(max(0, x-HINT_RADIUS), min(color_map.shape[1], x+HINT_RADIUS+1)):
                for y_ in range(max(0, y-HINT_RADIUS), min(color_map.shape[0], y+HINT_RADIUS+1)):
                    color_map[y_, x_, 0] = color.red() / 255.0
                    color_map[y_, x_, 1] = color.green() / 255.0
                    color_map[y_, x_, 2] = color.blue() / 255.0
                    mask[y_, x_, 0] = 1.0

        color_map = np.pad(color_map, padding, 'edge')
        mask = np.pad(mask, padding, 'edge')

        # from matplotlib import pyplot as plt
        # plt.imsave('hint_map.png', color_map)
        # plt.imsave('mask.png', np.minimum(np.concatenate([mask]*3, axis=2), 1.0))

        return color_map, mask

    def run(self):
        self.progress.emit('Preparing input')
        arr = qimage2ndarray.rgb_view(self.window.raw_image.fullsize_pixmap.toImage(), byteorder='big').copy()
        # arr[:, :, 0] -= np.minimum(arr[:, :, 0], 20)  # for testing purposes
        # arr[:, :, 2] -= np.minimum(arr[:, :, 2], 20)  # for testing purposes
        arr = arr.astype('float32') / 255.0
        arr = cv2.cvtColor(arr, cv2.COLOR_BGR2GRAY)
        self.window.colorizer.set_image(arr)
        self.window.colorizer.update_hint(*self.prepare_hints_mask(arr))
        self.progress.emit('Running colorization')
        arr = self.window.colorizer.colorize()
        arr = (arr * 255.0).astype('uint8')
        self.window.colorized_image.reload_pixmap(QtGui.QPixmap(qimage2ndarray.array2qimage(arr)))
        self.progress.emit('')
        self.finished.emit()


class MainWindow(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle('Colorize')

        self.colorization_progress_label.setText('')

        icon_filenames = {
            x.rsplit('.', 1)[0]: x
            for x in os.listdir('icons')
        }
        for mode in EDIT_MODES:
            button = getattr(self, f'{mode}_mode_button')
            icon = QtGui.QIcon(os.path.join('icons', icon_filenames[mode]))
            button.setIcon(icon)
            button.setText('')
            button.pressed.connect(partial(self.set_edit_mode, mode))
        self.set_edit_mode('tip')

        for property_name in ['size', 'opacity', 'hardness']:
            getattr(self, f'brush_{property_name}_slider').valueChanged.connect(self.brushSliderChanged(property_name))
            getattr(self, f'brush_{property_name}_input').textEdited.connect(self.brushInputChanged(property_name))
            getattr(self, f'brush_{property_name}_input').setValidator(QtGui.QIntValidator(0, 100))
            getattr(self, f'brush_{property_name}_slider').setValue(getattr(self.raw_image, f'brush_{property_name}'))
            getattr(self, f'brush_{property_name}_input').setText(str(getattr(self.raw_image, f'brush_{property_name}')))

        self.raw_folder_dialog_button.pressed.connect(partial(self.select_folder, 'raw'))
        self.save_folder_dialog_button.pressed.connect(partial(self.select_folder, 'save'))
        self.raw_images_list = []
        self.current_image_idx = None
        self.prev_image_button.pressed.connect(self.select_prev_image)
        self.next_image_button.pressed.connect(self.select_next_image)

        self.colorize_button.pressed.connect(self.colorize)
        # For testing purposes
        # self.select_folder('raw', '/Users/v-sopov/projects/hse/colorization/sample_images')

        self.save_button.pressed.connect(self.save)

        compute_device = 'cuda' if torch.cuda.is_available() else 'cpu'
        self.colorizer = MangaColorizator(
            compute_device,
            generator_path='weights/networks/generator1.zip',
            extractor_path='weights/networks/extractor.pth'
        )
        # self.colorize()


    def brushSliderChanged(self, property_name):
        def slot():
            slider_widget = getattr(self, f'brush_{property_name}_slider')
            input_widget = getattr(self, f'brush_{property_name}_input')
            canvas_property_name = f'brush_{property_name}'
            input_widget.setText(str(slider_widget.value()))
            setattr(self.raw_image, canvas_property_name, slider_widget.value())
            setattr(self.colorized_image, canvas_property_name, slider_widget.value())
        return slot

    def brushInputChanged(self, property_name):
        def slot():
            slider_widget = getattr(self, f'brush_{property_name}_slider')
            input_widget = getattr(self, f'brush_{property_name}_input')
            default_value = '1' if property_name == 'size' else '0'
            new_value = int(input_widget.text() or default_value)
            canvas_property_name = f'brush_{property_name}'
            slider_widget.setValue(new_value)
            setattr(self.raw_image, canvas_property_name, new_value)
            setattr(self.colorized_image, canvas_property_name, new_value)
        return slot

    def select_folder(self, destination, folder=None):
        if folder is None:
            folder = QtWidgets.QFileDialog.getExistingDirectory(
                self, 'Open Directory',
                os.getcwd(),
                QtWidgets.QFileDialog.ShowDirsOnly | QtWidgets.QFileDialog.DontResolveSymlinks
            )
        if folder:
            getattr(self, f'{destination}_folder_input').setText(folder)
            if destination == 'raw':
                self.save_folder_input.setText(os.path.join(folder, '__colorized__'))
                allowed_extensions = ['.jpg', '.jpeg', '.png', '.bmp']
                self.raw_images_list = sorted([
                    x for x in os.listdir(folder)
                    if any(x.endswith(ext) for ext in allowed_extensions)
                ])
                if self.raw_images_list:
                    self.current_image_idx = 0
                    self.current_image_label.setText(self.raw_images_list[0])
                    self.raw_image.reload_pixmap(os.path.join(self.raw_folder_input.text(), self.raw_images_list[self.current_image_idx]))
                else:
                    self.current_image_idx = None
                    self.current_image_label.setText('<NO IMAGES FOUND>')

    def select_prev_image(self):
        if self.current_image_idx is not None:
            self.current_image_idx = (self.current_image_idx - 1) % len(self.raw_images_list)
            self.load_image_by_idx()

    def select_next_image(self):
        if self.current_image_idx is not None:
            self.current_image_idx = (self.current_image_idx + 1) % len(self.raw_images_list)
            self.load_image_by_idx()

    def load_image_by_idx(self):
            current_image = self.raw_images_list[self.current_image_idx]
            self.current_image_label.setText(current_image)
            self.raw_image.reload_pixmap(os.path.join(self.raw_folder_input.text(), current_image))
            self.colorized_image.reload_pixmap(QtGui.QPixmap(qimage2ndarray.array2qimage(np.zeros(shape=(256, 256, 3)))))

    def colorize(self):
        self.colorization_thread = QtCore.QThread()
        self.colorization_worker = ColorizerWorker(self)
        self.colorization_worker.moveToThread(self.colorization_thread)
        self.colorization_thread.started.connect(self.colorization_worker.run)
        self.colorization_worker.finished.connect(self.colorization_thread.quit)
        self.colorization_worker.finished.connect(self.colorization_worker.deleteLater)
        self.colorization_thread.finished.connect(self.colorization_thread.deleteLater)
        self.colorization_worker.progress.connect(self.reportColorizationProgress)
        self.colorize_button.setEnabled(False)
        self.colorization_thread.finished.connect(
            lambda: self.colorize_button.setEnabled(True)
        )
        self.colorization_thread.start()

    def reportColorizationProgress(self, new_text):
        self.colorization_progress_label.setText(new_text)

    def save(self):
        current_image_name = self.raw_images_list[self.current_image_idx]
        save_folder = self.save_folder_input.text()
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        save_path = os.path.join(save_folder, current_image_name)
        image = self.colorized_image.fullsize_pixmap.toImage()
        image.save(save_path)

    def set_edit_mode(self, new_mode):
        for mode in EDIT_MODES:
            button = getattr(self, f'{mode}_mode_button')
            if mode != new_mode:
                button.setStyleSheet('padding: 2px 3px; border: none')
            else:
                button.setStyleSheet('padding: 2px 2px; border: 1px solid black')
        self.raw_image.edit_mode = new_mode
        self.colorized_image.edit_mode = new_mode




def main():
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()


if __name__ == '__main__':
    main()