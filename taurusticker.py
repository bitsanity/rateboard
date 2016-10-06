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

class TaurusTicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(TaurusTicker, self).__init__(parent)
    self.p_model = Taurus( targetCurr )
    self.initUI()

  def initUI(self):
    super(TaurusTicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/taurus.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(TaurusTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(),
                 'Taurus BTC' + self.p_model.getTargetCurr() )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row2y() - 5,
                 'bid: ' + self.p_model.getBestBid() )
    qp.drawText( self.b_col1x(), self.b_row3y() - 5,
                 'ask: ' + self.p_model.getBestAsk() )

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

class Taurus(Modellet):
  def __init__(self, targetCurr='CAD'):
    self.p_targetCurr = targetCurr
    self.p_refreshTime = None
    self.p_bestBid = '000.00'
    self.p_bestAsk = '000.00'

  def getBestBid(self):
    return self.p_bestBid

  def getBestAsk(self):
    return self.p_bestAsk

  def getAsk(self):
    return self.p_bestAsk

  def getTargetCurr(self):
    return self.p_targetCurr

  def doRefresh(self):
    req = 'https://https://api.taurusexchange.com/ticker'

    try:
      resp = urllib2.urlopen(req).read()

      self.p_bestBid = json.loads(resp)['bid']
      self.p_bestAsk = json.loads(resp)['ask']
      super(Taurus, self).setFaultFlag(False)
      super(Taurus, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(Taurus, self).setFaultFlag(True)

