#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys, traceback
import threading
import time

from PyQt4 import QtGui,QtCore

from boardlet import Boardlet
from modellet import Modellet

class MyTicker(Boardlet):
  def __init__(self, parent, getbidobj, getaskobj):
    super(MyTicker, self).__init__(parent)
    self.p_model = MyModel(getbidobj, getaskobj)
    self.initUI()

  def initUI(self):
    super(MyTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/my.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(MyTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(), 'My Rates (USD)' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row2y() - 5,
                 'buy: ' + self.p_model.getBuy() )
    qp.drawText( self.b_col1x(), self.b_row3y() - 5,
                 'sell: ' + self.p_model.getSell() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( self.b_imgx(), self.b_row4y(),
                 'Refreshed: ' + self.p_model.getLastUpdated() )
    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

class MyModel(Modellet):
  def __init__(self, getbidobj, getaskobj):
    self.p_refreshTime = None
    self.p_buy = '000.00'
    self.p_sell = '000.00'
    self.p_bidobj = getbidobj
    self.p_askobj = getaskobj

  def getBuy(self):
    return self.p_buy

  def getSell(self):
    return self.p_sell

  def doRefresh(self):
    try:
      self.p_buy = "%.2f" % (float(self.p_bidobj.getBid()) * 0.98)
      self.p_sell = "%.2f" % (float(self.p_askobj.getAsk()) * 1.02)

      super(MyModel, self).setFaultFlag(False)
      super(MyModel, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(MyModel, self).setFaultFlag(True)

