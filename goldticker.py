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
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/img/gold.png' ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(GoldTicker, self).paintEvent(e)

    if None == self.p_model.getData():
      return

    try:
      source = QtGui.QImage()
      source.loadFromData( self.p_model.getData() )
      source = source.copy( 0,0, source.width(), 100 )

      # substitute 'black' pixels with transparent
      dest = QtGui.QImage( source.width(), source.height(),
                           QtGui.QImage.Format_ARGB32 )

      qp = QtGui.QPainter()
      qp.begin( dest )

      for col in xrange(0, source.width()):
        for row in xrange(0, source.height()):
          pel = QtGui.QColor( source.pixel(col, row) )
          if pel.red() < 10 and pel.green() < 10 and pel.blue() < 10:
            dest.setPixel( col, row, QtGui.qRgba(0,0,0,0) )
          else:
            dest.setPixel( col, row, pel.rgba() )
      qp.end()

      # draw on screen
      qp = QtGui.QPainter()
      qp.begin(self)
      qp.drawImage( self.b_col1x(), self.b_imgy(), dest )
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

