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

class GoldTicker(Boardlet):
  def __init__(self, parent):
    super(GoldTicker, self).__init__(parent)
    self.p_model = GoldRate()
    self.fubar()

  def fubar(self):
    super(GoldTicker, self).initUI()

    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/gold.png' ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(GoldTicker, self).paintEvent(e)

    if None == self.p_model.getData():
      return

    try:
      pixmap = QtGui.QPixmap()
      pixmap.loadFromData( self.p_model.getData() )
      width = pixmap.width()
      pixmap = pixmap.copy( 0,0, width, 100 )

      qp = QtGui.QPainter()
      qp.begin(self)
      qp.drawPixmap( 99, 19, pixmap )
      qp.end()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      self.p_model.doRefresh()
      time.sleep( st )

class GoldRate(Modellet):
  def __init__(self):
    super(GoldRate, self).__init__()
    self.p_imgdata = None

  def getData(self):
    return self.p_imgdata

  def doRefresh(self):
    url = 'http://www.kitconet.com/images/quotes_special.gif'

    try:
      self.p_imgdata = urllib2.urlopen(url).read()

      super(GoldRate, self).setFaultFlag(False)
      super(GoldRate, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(GoldRate, self).setFaultFlag(True)

