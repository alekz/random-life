import sys
import math
from PyQt4 import QtCore, QtGui

class LifeApplication(QtGui.QApplication):

    def __init__(self, life, fps=0):

        super(LifeApplication, self).__init__(sys.argv)

        self.life = life
        if fps > 0:
            self.timer_delay = 1000 / fps
            self.timer_delay = max(1, self.timer_delay)
            self.timer_delay = min(1000, self.timer_delay)
        else:
            self.timer_delay = 1

        self.widget = Canvas(life)
        self.widget.show()


    def exec_(self):

        # Create and start timer
        self.timer = QtCore.QTimer()
        self.connect(self.timer, QtCore.SIGNAL('timeout()'), self.updateLife)
        self.timer.setSingleShot(True)
        self.timer.start(self.timer_delay)

        # Run the application
        return super(LifeApplication, self).exec_()

    def updateLife(self):
        self.life.next()
        self.widget.repaint()
        self.timer.start(self.timer_delay)

class Canvas(QtGui.QWidget):

    def __init__(self, life):

        self.life = life

        super(Canvas, self).__init__()

        self.setFixedSize(800, 800)
        self.setWindowTitle('Life')

    def paintEvent(self, e):
        painter = Painter(self)
        painter.fillBackground()
        painter.drawLife(self.life)

class Painter(QtGui.QPainter):

    def fillBackground(self):
        self.fillRect(0, 0, self.device().width(), self.device().height(), QtGui.QColor('black'))

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
