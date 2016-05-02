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

class CoinbaseTicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(CoinbaseTicker, self).__init__(parent)
    self.p_model = Coinbase( targetCurr )
    self.initUI()

  def initUI(self):
    super(CoinbaseTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/coinbase.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(CoinbaseTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 32, 'Coinbase BTC' + self.p_model.getTargetCurr() )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( 85, 55, 'bid: ' + self.p_model.getBestBid() )
    qp.drawText( 85, 75, 'ask: ' + self.p_model.getBestAsk() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( 20, 94, 'Refreshed: ' + self.p_model.getLastUpdated() )

    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

class Coinbase(Modellet):
  def __init__(self, targetCurr='EUR'):
    self.p_targetCurr = targetCurr
    self.p_refreshTime = None
    self.p_bestBid = '000.00'
    self.p_bestAsk = '000.00'

  def getBestBid(self):
    return self.p_bestBid

  def getBestAsk(self):
    return self.p_bestAsk

  def getTargetCurr(self):
    return self.p_targetCurr

  def doRefresh(self):
    req = 'https://api.exchange.coinbase.com/products/BTC-' + self.p_targetCurr + '/book'

    try:
      resp = urllib2.urlopen(req).read()
      #resp = '{"sequence":224989842,"bids":[["228.09","3.017",1]],"asks":[["228.13","0.01",1]]}'

      self.p_bestBid = json.loads(resp)['bids'][0][0]
      self.p_bestAsk = json.loads(resp)['asks'][0][0]
      super(Coinbase, self).setFaultFlag(False)
      super(Coinbase, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(Coinbase, self).setFaultFlag(True)

