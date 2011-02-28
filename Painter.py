import math

from PyQt4 import QtGui
#from LifeManager import LifeManager

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
