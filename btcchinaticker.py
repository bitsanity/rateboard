#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys, traceback
import threading
import time
import simplejson as json
import urllib2

from PyQt4 import QtGui,QtCore
import threading

from boardlet import Boardlet
from modellet import Modellet

class BTCChinaTicker(Boardlet):
  def __init__(self, parent):
    super(BTCChinaTicker, self).__init__(parent)
    self.p_model = BTCChina()
    self.initUI()

  def initUI(self):
    super(BTCChinaTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/btcchina.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(BTCChinaTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(), 'BTCChina BTCCNY' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row2y() - 5,
                 'buy: ' + self.p_model.getBuy() )
    qp.drawText( self.b_col1x(), self.b_row3y() - 5,
                 'sell: ' + self.p_model.getSell() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( self.b_imgx(), 94,
                 'Refreshed: ' + self.p_model.getLastUpdated() )

    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

class BTCChina(Modellet):
  def __init__(self):
    self.p_refreshTime = None
    self.p_buy = '0000.00'
    self.p_sell = '0000.00'

  def getBuy(self):
    return self.p_buy

  def getSell(self):
    return self.p_sell

  def doRefresh(self):
    req = 'https://data.btcchina.com/data/ticker'

    try:
      resp = urllib2.urlopen(req).read()
      #resp = '{"ticker":{"high":"1475.88","low":"1440.00","buy":"1448.97","sell":"1449.70","last":"1449.74","vol":"17255.70510000","date":1441138258,"vwap":"1452.87","prev_close":"1466.52","open":"1466.14"}}'

      rdict = json.loads( resp )
      self.p_buy = rdict['ticker']['buy']
      self.p_sell = rdict['ticker']['sell']

      super(BTCChina, self).setFaultFlag(False)
      super(BTCChina, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(BTCChina, self).setFaultFlag(False)

