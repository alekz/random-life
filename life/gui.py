import sys
import math
from PyQt4 import QtCore, QtGui

class LifeApplication(QtGui.QApplication):

    # Initialize
    def __init__(self, life):

        QtGui.QApplication.__init__(self, sys.argv)

        self.life = life

        self.widget = Canvas(life)
        self.widget.show()


    # Run application
    def exec_(self):

        # Create timer
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateLife)
        self.timer.setSingleShot(True)
        self.timer.start(100)

        # Run
        return QtGui.QApplication.exec_()

    # Updates life
    def updateLife(self):
        self.life.next()
        self.widget.repaint()
        self.timer.start(1)

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

class Painter(QtGui.QPainter):

    # Fill background
    def fillBackground(self):
        self.fillRect(0, 0, self.device().width(), self.device().height(), QtGui.QColor('black'))

    # Draws Life
    def drawLife(self, life):

        # Calculate coefficients
        cx = self.device().width() / life.width()
        cy = self.device().height() / life.height()

        # Iterate through seeds
        for x in xrange(life.width()):
            for y in xrange(life.height()):
                if life.isAlive(x, y):

                    # Set color
                    c = life.color(x, y)
                    color = QtGui.QColor(c[0], c[1], c[2])
                    self.setPen(color)
                    self.setBrush(color)

                    # Calculate and draw rectangle
                    x1 = math.floor(cx * x)
                    y1 = math.floor(cy * y)
                    x2 = math.floor(cx * (x + 1)) - 1
                    y2 = math.floor(cy * (y + 1)) - 1
                    self.drawRect(x1, y1, x2 - x1 - 1, y2 - y1 - 1)
