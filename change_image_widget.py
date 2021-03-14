with open('form.py') as f:
    content = f.read()

import_string = 'from PyQt5 import QtCore, QtGui, QtWidgets\n'
content = content.replace(import_string, import_string + 'from draw import Canvas\n')

content = content.replace('self.raw_image = QtWidgets.QLabel(', 'self.raw_image = Canvas(')
# TODO: colorized image

with open('form.py', 'w') as f:
    f.write(content)