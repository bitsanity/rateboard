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

class CoindeskBPITicker(Boardlet):
  def __init__(self, parent, targetCurr):
    super(CoindeskBPITicker, self).__init__(parent)
    self.p_model = CoindeskBPI( targetCurr )
    self.initUI()

  def initUI(self):
    super(CoindeskBPITicker, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry( self.b_imgx(), self.b_imgy(),
                             self.b_iconwidth(),self.b_iconheight() )
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + "/img/coindesk.png" ) )

    t = threading.Thread(target=self.periodicUpdate)
    t.setDaemon(True)
    t.start()

  def paintEvent(self, e):
    super(CoindeskBPITicker, self).paintEvent(e)

    qp = QtGui.QPainter()
    qp.begin(self)
    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col1x(), self.b_row1y(), 'Coindesk BPI' )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row2y() - 5,
                 "{:08.2f}".format(self.p_model.getTargetPrice()) )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col2x() + 20, self.b_row2y() - 5,
                 self.p_model.getTargetCurr() )
    qp.setFont( self.p_normFont )
    qp.drawText( self.b_col1x(), self.b_row3y() - 5,
                 "{:08.2f}".format(self.p_model.getUSDPrice()) )
    qp.setFont( self.p_pairFont )
    qp.drawText( self.b_col2x() + 20, self.b_row3y() - 5, 'USD' )

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

class CoindeskBPI(Modellet):
  def __init__(self, targetCurr='EUR'):
    self.p_targetCurr = targetCurr
    self.p_refreshTime = None
    self.p_usdPrice = '0,000.00'
    self.p_targetPrice = '0,000.00'

  def getTargetPrice(self):
    return float(self.p_targetPrice.replace(',',''))

  def getTargetCurr(self):
    return self.p_targetCurr

  def getUSDPrice(self):
    return float(self.p_usdPrice.replace(',',''))

  def doRefresh(self):
    req = 'http://api.coindesk.com/v1/bpi/currentprice/' + self.p_targetCurr + '.json'

    try:
      resp = urllib2.urlopen(req).read()
      #resp = '{"time":{"updated":"Aug 26, 2015 16:34:00 UTC","updatedISO":"2015-08-26T16:34:00+00:00","updateduk":"Aug 26, 2015 at 17:34 BST"},"disclaimer":"This data was produced from the CoinDesk Bitcoin Price Index (USD). Non-USD currency data converted using hourly conversion rate from openexchangerates.org","bpi":{"USD":{"code":"USD","rate":"228.4804","description":"United States Dollar","rate_float":228.4804},"' + self.p_targetCurr + '":{"code":"' + self.p_targetCurr + '","rate":"303.6635","description":"Canadian Dollar","rate_float":303.6635}}}'

      bpidict = json.loads(resp)['bpi']
      self.p_usdPrice = bpidict['USD']['rate']
      self.p_targetPrice = bpidict[self.p_targetCurr]['rate']
      super(CoindeskBPI, self).setFaultFlag(False)
      super(CoindeskBPI, self).setLastUpdatedNow()
    except Exception:
      exc_type, exc_value, exc_traceback = sys.exc_info()
      lines = traceback.format_exception(exc_type, exc_value, exc_traceback)
      print ''.join('!! ' + line for line in lines)
      super(CoindeskBPI, self).setFaultFlag(False)

