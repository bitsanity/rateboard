#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys, traceback
import threading
import time
import simplejson as json

import urllib2

from PyQt4 import QtGui,QtCore

from boardlet import Boardlet
from modellet import Modellet

class SouthxTicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(SouthxTicker, self).__init__(parent)
    self.p_model = Southx( targetCurr )
    self.initUI()

  def initUI(self):
    super(SouthxTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/bch.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(SouthxTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(), 'Southx BCHUSD' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row2y() - 5,
                 'bid: ' + "{:09.4f}".format(self.p_model.getBid()) )
    qp.drawText( self.b_col1x(), self.b_row3y() - 5,
                 'ask: ' + "{:09.4f}".format(self.p_model.getAsk()) )

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

class Southx(Modellet):
  def __init__(self, targetCurr='usd'):
    self.p_targetCurr = targetCurr
    self.p_refreshTime = None
    self.p_bid = '000.00'
    self.p_ask = '000.00'

  def getBid(self):
    return float(self.p_bid)

  def getAsk(self):
    return float(self.p_ask)

  def getTargetCurr(self):
    return self.p_targetCurr

  def doRefresh(self):
    headers = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request( 'https://www.southxchange.com/api/price/BCH/USD',
                           None, headers )

    try:
      resp = urllib2.urlopen(req).read()
      rdict = json.loads( resp )
      self.p_bid = rdict['Bid']
      self.p_ask = rdict['Ask']

      super(Southx, self).setFaultFlag(False)
      super(Southx, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(Southx, self).setFaultFlag(False)

