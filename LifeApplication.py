import sys
from PyQt4 import QtCore
from PyQt4 import QtGui
from Canvas import Canvas

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
