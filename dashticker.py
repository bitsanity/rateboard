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

class DashTicker(Boardlet):
  def __init__(self, parent, btcusd):
    super(DashTicker, self).__init__(parent)
    self.p_model = Dash( btcusd )
    self.initUI()

  def initUI(self):
    super(DashTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/dash.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(DashTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(), 'Bittrex DASHUSD' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row2y() - 5,
                 'bid: ' + "{:06.2f}".format(self.p_model.getBestBid()) )
    qp.drawText( self.b_col1x(), self.b_row3y() - 5,
                 'ask: ' + "{:06.2f}".format(self.p_model.getBestAsk()) )

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

class Dash(Modellet):
  def __init__(self, btcusd):
    self.p_btcusd = btcusd
    self.p_refreshTime = None
    self.p_bestBid = '000.00'
    self.p_bestAsk = '000.00'

  def getBestBid(self):
    return float(self.p_bestBid) * float(self.p_btcusd.p_model.getBid())

  def getBestAsk(self):
    return float(self.p_bestAsk) * float(self.p_btcusd.p_model.getAsk())

  def doRefresh(self):
    headers = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request( 'https://bittrex.com/api/v1.1/public/getticker?market=BTC-DASH', None, headers )

    try:
      resp = urllib2.urlopen(req).read()
      self.p_bestBid = str( json.loads(resp)['result']['Bid'] )
      self.p_bestAsk = str( json.loads(resp)['result']['Ask'] )
      super(Dash, self).setFaultFlag(False)
      super(Dash, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(Dash, self).setFaultFlag(True)

