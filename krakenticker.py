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

class KrakenTicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(KrakenTicker, self).__init__(parent)
    self.p_model = KrakenRatesModellet( targetCurr )
    self.initUI()

  def initUI(self):
    super(KrakenTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/kraken.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(KrakenTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)

    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 32, 'Kraken XBT/' + self.p_model.getTargetCurr()  )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( 85, 55, 'bid: ' + self.p_model.getBid() )
    qp.drawText( 85, 74, 'ask: ' + self.p_model.getBid() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( 20, 94, 'Refreshed: ' + self.p_model.getLastUpdated() )

    ch = self.p_model.getPercentageChange()
    if '+' in ch:
      qp.setPen( self.p_greenPen )
    else:
      qp.setPen( self.p_redPen )
    qp.drawText( 150, 94, ch )
    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

class KrakenRatesModellet(Modellet):
  def __init__(self, targetCurr):
    super(KrakenRatesModellet, self).__init__()
    self.p_targetCurr = targetCurr
    self.p_refreshTime = None
    self.p_ask = '000.00'
    self.p_bid = '000.00'
    self.p_openingPrice = '000.00'
    self.p_lastTrade = '000.00'

  def getAsk(self):
    return self.p_ask

  def getBid(self):
    return self.p_bid

  def getOpeningPrice(self):
    return self.p_openingPrice

  def getLastTradePrice(self):
    return self.p_lastTrade

  def getTargetCurr(self):
    return self.p_targetCurr

  def getPercentageChange(self):
    of = float(self.p_openingPrice)
    lf = float(self.p_lastTrade)

    if 0.0 < of:
      pct = ((lf - of) / of) * 100.0
    else:
      pct = 0.0

    result = '%.4f' % pct
    if lf >= of:
      result = '+' + result

    return result + '%'

  def doRefresh(self):
    req = 'https://api.kraken.com/0/public/Ticker?pair=XBT' + self.p_targetCurr
    headers = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request( req, None, headers )

    try:
      resp = urllib2.urlopen(req).read()
      #resp = '{"error":[],"result":{"XXBTZUSD":{"a":["228.80540","1","1.000"],"b":["228.03260","2","2.000"],"c":["229.71480","0.24347582"],"v":["97.21314340","116.72196730"],"p":["232.72008","231.35622"],"t":[277,310],"l":["223.11341","223.11341"],"h":["243.37880","243.37880"],"o":"224.49439"}}}'

      rdict = json.loads(resp)['result']['XXBTZ' + self.p_targetCurr]
      self.p_ask = rdict['a'][0]
      self.p_bid = rdict['b'][0]
      self.p_lastTrade = rdict['c'][0]
      self.p_openingPrice = rdict['o']

      super(KrakenRatesModellet, self).setFaultFlag(False)
      super(KrakenRatesModellet, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(KrakenRatesModellet, self).setFaultFlag(True)
