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

class QuadrigaTicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(QuadrigaTicker, self).__init__(parent)
    self.p_model = Quadriga( targetCurr )
    self.initUI()

  def initUI(self):
    super(QuadrigaTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/quadriga.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(QuadrigaTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 32, 'Quadriga BTC' + self.p_model.getTargetCurr() )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( 85, 55, 'bid: ' + self.p_model.getBid() )
    qp.drawText( 85, 75, 'ask: ' + self.p_model.getAsk() )

    qp.setFont( self.p_timeFont )
    qp.setPen( self.p_grayPen )
    qp.drawText( 20, 94, 'Refreshed: ' + self.p_model.getLastUpdated() )

    qp.end()

  def periodicUpdate(self):
    while(True):
      st = self.getNextWaitTimeSeconds()
      time.sleep( st )
      self.p_model.doRefresh()

class Quadriga(Modellet):
  def __init__(self, targetCurr='cad'):
    self.p_targetCurr = targetCurr
    self.p_refreshTime = None
    self.p_bid = '000.00'
    self.p_ask = '000.00'

  def getBid(self):
    return self.p_bid

  def getAsk(self):
    return self.p_ask

  def getTargetCurr(self):
    return self.p_targetCurr

  def doRefresh(self):
    headers = {'User-agent' : 'Mozilla/5.0'}
    req = urllib2.Request('https://api.quadrigacx.com/v2/ticker?book=btc_' + self.p_targetCurr, None, headers )

    try:
      resp = urllib2.urlopen(req).read()
      rdict = json.loads( resp )
      self.p_bid = rdict['bid']
      self.p_ask = rdict['ask']

      super(Quadriga, self).setFaultFlag(False)
      super(Quadriga, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(Quadriga, self).setFaultFlag(False)

