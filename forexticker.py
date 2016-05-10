#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import sys, traceback
import threading
import time
import urllib2

from PyQt4 import QtGui,QtCore

from boardlet import Boardlet
from modellet import Modellet

class ForexTicker(Boardlet):
  def __init__(self, parent, currPair):
    super(ForexTicker, self).__init__(parent)
    self.p_model = ForexRate( currPair )
    self.fubar()

  def fubar(self):
    super(ForexTicker, self).initUI()

    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )

    if 'CAD' in self.p_model.getCurrPair():
      self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/img/cad.png' ) )
    elif 'GBP' in self.p_model.getCurrPair():
      self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/img/gbp.png' ) )
    elif 'EUR' in self.p_model.getCurrPair():
      self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/img/eur.png' ) )
    elif 'CNY' in self.p_model.getCurrPair():
      self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/img/cny.png' ) )
    else:
      self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/img/globe.png' ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(ForexTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)

    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(), self.p_model.getCurrPair() )
    qp.drawText( self.b_col2x() + 15, self.b_row1y(), 'Inverse' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_rateFont )

    rt = self.p_model.getRate()
    qp.drawText( self.b_col1x(), self.b_row2y(), rt )

    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col2x() + 15, self.b_row2y(), self.inverseOf(rt) )

    qp.setFont( self.p_timeFont )
    ch = self.p_model.getChange()
    if None != ch and '-' in ch:
      qp.setPen( self.p_redPen )
    else:
      qp.setPen( self.p_greenPen )
    qp.drawText( self.b_col1x(), self.b_row3y() - 3, ch )

    qp.setPen( self.p_grayPen )
    qp.drawText( self.b_imgx(), self.b_row4y(),
                 'Refreshed: ' + self.p_model.getLastUpdated() )

    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

class ForexRate(Modellet):
  def __init__(self, currPair=None):  # e.g. 'USDEUR'
    super(ForexRate, self).__init__()

    self.p_currPair = currPair
    self.p_rate = '0.0000'
    self.p_change = '+00.00%'

  def getRate(self):
    return self.p_rate

  def getChange(self):
    return self.p_change

  def getCurrPair(self):
    return self.p_currPair

  def doRefresh(self):
    # f param: s = symbol, l1 = last trade, c1 = change
    req = 'http://finance.yahoo.com/d/quotes.csv?s=' + self.p_currPair + '=X&f=sl1c1'

    try:
      resp = urllib2.urlopen(req)
      cr = csv.reader(resp)
      for row in cr:
        self.p_rate = row[1]
        self.p_change = row[2]

      super(ForexRate, self).setFaultFlag(False)
      super(ForexRate, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(ForexRate, self).setFaultFlag(False)

