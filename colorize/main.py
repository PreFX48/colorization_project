from functools import partial
import os
import sys

import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt
import qimage2ndarray

import form


EDIT_MODES = ['brush', 'colorpicker', 'eraser', 'fill']


class MainWindow(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        icon_filenames = {
            x.rsplit('.', 1)[0]: x
            for x in os.listdir('icons')
        }
        for mode in EDIT_MODES:
            button = getattr(self, f'{mode}_mode_button')
            print(button.styleSheet())
            icon = QtGui.QIcon(os.path.join('icons', icon_filenames[mode]))
            button.setIcon(icon)
            button.setText('')
            button.pressed.connect(partial(self.set_edit_mode, mode))
        self.set_edit_mode('brush')

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
        # self.colorize()

        self.save_button.pressed.connect(self.save)


    def brushSliderChanged(self, property_name):
        def slot():
            slider_widget = getattr(self, f'brush_{property_name}_slider')
            input_widget = getattr(self, f'brush_{property_name}_input')
            canvas_property_name = f'brush_{property_name}'
            input_widget.setText(str(slider_widget.value()))
            setattr(self.raw_image, canvas_property_name, slider_widget.value())
            # TODO: colorized image
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
            # TODO: colorized image
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
        arr = qimage2ndarray.rgb_view(self.raw_image.original_pixmap.toImage(), byteorder='big').copy()
        arr[:, :, 0] -= np.minimum(arr[:, :, 0], 20)
        arr[:, :, 2] -= np.minimum(arr[:, :, 2], 20)
        self.colorized_image.original_pixmap = QtGui.QPixmap(qimage2ndarray.array2qimage(arr))
        self.colorized_image.updateScaledPixmap()

    def save(self):
        current_image_name = self.raw_images_list[self.current_image_idx]
        save_folder = self.save_folder_input.text()
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        save_path = os.path.join(save_folder, current_image_name)
        image = self.colorized_image.original_pixmap.toImage()
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