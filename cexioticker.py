#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys, traceback
import threading
import time
from PyQt4 import QtGui,QtCore
import threading
import urllib2

from boardlet import Boardlet
from modellet import Modellet

class CEXIOTicker(Boardlet):
  def __init__(self, parent):
    super(CEXIOTicker, self).__init__(parent)
    self.p_model = CEXIOModellet()
    self.initUI()

  def initUI(self):
    super(CEXIOTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/cexio.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(CEXIOTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)

    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 32, 'CEX.IO XBTUSD' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_rateFont )
    qp.drawText( 85, 66, self.p_model.getLastPrice() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( 20, 94, 'Refreshed: ' + self.p_model.getLastUpdated() )
    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()
      self.update()

class CEXIOModellet(Modellet):
  p_req = 'https://cex.io/api/last_price/BTC/USD'

  def __init__(self):
    super(CEXIOModellet, self).__init__()
    self.p_lastPrice = '000.0000'

  def getLastPrice(self):
    return self.p_lastPrice

  def doRefresh(self):
    headers = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request( self.p_req + self.p_targetCurr, None, headers )

    try:
      resp = urllib2.urlopen(req).read()
      #resp = '{"lprice":"226.539"}'
      rdict = json.loads(resp)
      self.p_lastPrice = rdict['lprice']
      super(CEXIOModellet, self).setFaultFlag(False)
      super(CEXIOModellet, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(CEXIOModellet, self).setFaultFlag(True)
