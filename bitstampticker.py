#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys, traceback
import threading
import time
from PyQt4 import QtGui,QtCore

import simplejson as json
import urllib2

from boardlet import Boardlet
from modellet import Modellet

class BitstampTicker(Boardlet):
  def __init__(self, parent ):
    super(BitstampTicker, self).__init__(parent)
    self.p_model = BitstampModellet()
    self.initUI()

  def initUI(self):
    super(BitstampTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/bitstamp.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(BitstampTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)

    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 32, 'Bitstamp' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 56, 'BTCUSD: ' )
    qp.drawText( 85, 75, 'EURUSD: ' )
    qp.setFont( self.p_normFont )
    qp.drawText( 160, 56, self.p_model.getBid() + '/' + self.p_model.getAsk() )
    qp.drawText( 160, 75, self.p_model.getBuy() + '/' + self.p_model.getSell() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( 20, 94, 'Refreshed: ' + self.p_model.getLastUpdated() )
    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

# Bitstamp gives bid/ask for BTCUSD and buy/sell for EURUSD
class BitstampModellet(Modellet):

  btcReq = 'https://www.bitstamp.net/api/ticker/'
  eurReq = 'https://www.bitstamp.net/api/eur_usd/'

  def __init__(self):
    super(BitstampModellet, self).__init__()
    self.p_ask = '000.00'
    self.p_bid = '000.00'
    self.p_buy = '000.00'
    self.p_sell = '000.00'

  def getAsk(self):
    return self.p_ask

  def getBid(self):
    return self.p_bid

  def getBuy(self):
    return self.p_buy

  def getSell(self):
    return self.p_sell

  def doRefresh(self):
    try:
      resp = urllib2.urlopen(self.btcReq).read()
      #resp = '{"high": "231.09", "last": "225.10", "timestamp": "1440641676", "bid": "225.10", "vwap": "226.46", "volume": "24345.06718549", "low": "219.77", "ask": "225.30"}'

      rdict = json.loads(resp)
      self.p_ask = rdict['ask']
      self.p_bid = rdict['bid']

      resp = urllib2.urlopen(self.eurReq).read()
      #resp = '{"sell": "1.1415", "buy": "1.1523"}'
      rdict = json.loads(resp)
      self.p_buy = rdict['buy']
      self.p_sell = rdict['sell']

      super(BitstampModellet, self).setFaultFlag(False)
      super(BitstampModellet, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(BitstampModellet, self).setFaultFlag(True)

