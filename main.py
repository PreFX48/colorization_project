import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

import form


class MainWindow(QtWidgets.QMainWindow, form.Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)

        for property_name in ['size', 'opacity', 'hardness']:
            getattr(self, f'brush_{property_name}_slider').valueChanged.connect(self.brushSliderChanged(property_name))
            getattr(self, f'brush_{property_name}_input').textEdited.connect(self.brushInputChanged(property_name))
            getattr(self, f'brush_{property_name}_input').setValidator(QtGui.QIntValidator(0, 100))
            getattr(self, f'brush_{property_name}_slider').setValue(getattr(self.raw_image, f'brush_{property_name}'))
            getattr(self, f'brush_{property_name}_input').setText(str(getattr(self.raw_image, f'brush_{property_name}')))


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


app = QtWidgets.QApplication(sys.argv)
window = MainWindow()
window.show()
app.exec_()