#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import csv
import simplejson as json
import sys, traceback
import threading
import time
import urllib2

from PyQt4 import QtGui,QtCore

import simplejson as json

from boardlet import Boardlet
from modellet import Modellet

class BitpayTicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(BitpayTicker, self).__init__(parent)
    self.p_model = BitpayModellet( targetCurr )
    self.initUI()

  def initUI(self):
    super(BitpayTicker, self).initUI()

    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(self.b_imgx(),self.b_imgy(),56,56)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/bitpay.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(BitpayTicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)

    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(),
                 'Bitpay BTC' + self.p_model.getCurrPair() )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_rateFont )
    qp.drawText( self.b_col1x(), self.b_row2y(), self.p_model.getRate() )

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

class BitpayModellet(Modellet):
  def __init__(self, targetCurr=None):
    super(BitpayModellet, self).__init__()
    self.p_targetCurr = targetCurr
    self.p_rate = '000.00'

  def getRate(self):
    return self.p_rate

  def getCurrPair(self):
    return self.p_targetCurr

  def doRefresh(self):
    req = 'https://bitpay.com/rates/' + self.p_targetCurr

    try:
      resp = urllib2.urlopen(req).read()
      #resp = '{"data":{"code":"CAD","name":"Canadian Dollar","rate":299.826116}}'
      ratf = float(json.loads(resp)['data']['rate'])
      self.p_rate = '%.4f' % ratf

      super(BitpayModellet, self).setFaultFlag(False)
      super(BitpayModellet, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)

      super(BitpayModellet, self).setFaultFlag(False)

