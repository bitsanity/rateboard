from random import randint
from PyQt4 import QtGui,QtCore

class Boardlet(QtGui.QWidget):
  def __init__(self, parent):
    super(Boardlet, self).__init__(parent)

    # define fonts and pens here, once, for consistent style throughout subclasses
    self.p_grayPen = QtGui.QPen(QtCore.Qt.gray, 1, QtCore.Qt.SolidLine)
    self.p_blackPen = QtGui.QPen(QtCore.Qt.black, 1, QtCore.Qt.SolidLine)
    self.p_whitePen = QtGui.QPen( QtCore.Qt.white, 1, QtCore.Qt.SolidLine )
    self.p_greenPen = QtGui.QPen( QtCore.Qt.green, 1, QtCore.Qt.SolidLine )
    self.p_yellowPen = QtGui.QPen( QtCore.Qt.yellow, 1, QtCore.Qt.SolidLine )
    self.p_redPen = QtGui.QPen( QtCore.Qt.red, 1, QtCore.Qt.SolidLine )
    self.p_pairFont = QtGui.QFont('Helvetica', 12, QtGui.QFont.Bold)
    self.p_normFont = QtGui.QFont('Helvetica', 14, QtGui.QFont.Bold)
    self.p_rateFont = QtGui.QFont('Helvetica', 24, QtGui.QFont.Bold)
    self.p_timeFont = QtGui.QFont('Helvetica', 8)
    self.initUI()

  def initUI(self):
    self.setMinimumSize(300, 120)
    self.setMaximumSize(300, 120)

  def paintEvent(self, e):
    size = self.size()
    w = size.width()
    h = size.height()
    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    polyg = QtGui.QPolygon( [QtCore.QPoint(0,h-1),
                             QtCore.QPoint(0,0),
                             QtCore.QPoint(w-1,0)] )
    qp.drawPolyline(polyg)
    qp.setPen(self.p_blackPen)
    polyg = QtGui.QPolygon( [QtCore.QPoint(w-1,0),
                             QtCore.QPoint(w-1,h-1),
                             QtCore.QPoint(0,h-1)] )
    qp.drawPolyline(polyg)
    qp.end()

  def getNextWaitTimeSeconds(self):
    result = 15 * 60
    adj = randint(0, 5) * 60

    if 0 == randint( 0, 1 ):
      result = result - adj
    else:
      result = result + adj
    return result

  def inverseOf(self, fStr ):
    ff = float( fStr )

    if 0.0 != ff:
      resf = 1.00 / ff
    else:
      resf = 0.00

    return "%.4f" % resf
