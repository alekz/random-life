from PyQt4 import QtGui
from Painter import Painter

# Canvas class
class Canvas(QtGui.QWidget):

    # Initializes widget with Life
    def __init__(self, life):

        self.life = life

        QtGui.QWidget.__init__(self)

        self.setFixedSize(800, 800)
        self.setWindowTitle('Life')

    # Repaint widget
    def paintEvent(self, e):
        painter = Painter(self)
        painter.fillBackground()
        painter.drawLife(self.life)
