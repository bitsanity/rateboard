#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import sys
from PyQt4 import QtGui,QtCore

from boardlet import Boardlet
from clockboardlet import ClockBoardlet
from forexticker import ForexTicker
from coindeskbpiticker import CoindeskBPITicker
from krakenticker import KrakenTicker
from bitstampticker import BitstampTicker
from cexioticker import CEXIOTicker
from coinbaseticker import CoinbaseTicker
from btcchinaticker import BTCChinaTicker
from bitpayticker import BitpayTicker
from quadrigaticker import QuadrigaTicker

def go():
  app = QtGui.QApplication(sys.argv)
  mw = MainWindow()
  sys.exit(app.exec_())

class MainWindow(QtGui.QWidget):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.initUI()

  def initUI(self):
    self.setWindowTitle('Rate Board')

    rootWinRect = QtGui.QApplication.desktop().availableGeometry()
    pal = QtGui.QPalette()
    gradient = QtGui.QLinearGradient(0, 0, 0, rootWinRect.height())
    gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0))
    gradient.setColorAt(1.0, QtGui.QColor(0, 0, 255))
    pal.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
    self.setPalette( pal )

    van = ClockBoardlet(self, 'Vancouver')
    nyt = ClockBoardlet(self, 'New York')
    lot = ClockBoardlet(self, 'London')
    bet = ClockBoardlet(self, 'Beijing')
    frk = ClockBoardlet(self, 'Frankfurt')

    usdcad = ForexTicker(self, 'USDCAD')
    usdeur = ForexTicker(self, 'USDEUR')
    usdgbp = ForexTicker(self, 'USDGBP')
    usdcny = ForexTicker(self, 'USDCNY')

    #cd_cad = CoindeskBPITicker(self, 'CAD')
    cd_eur = CoindeskBPITicker(self, 'EUR')
    cd_gbp = CoindeskBPITicker(self, 'GBP')
    cd_cny = CoindeskBPITicker(self, 'CNY')

    kr_usd = KrakenTicker(self, 'USD')
    qu_us = QuadrigaTicker( self, 'USD' )
    qu_ca = QuadrigaTicker( self, 'CAD' )
    btstmp = BitstampTicker( self )
    #cexio = CEXIOTicker( self ) 403 Forbidden

    cbcad = CoinbaseTicker(self, 'CAD')
    cbusd = CoinbaseTicker(self, 'USD')
    cbgbp = CoinbaseTicker(self, 'GBP')
    cbeur = CoinbaseTicker(self, 'EUR')

    btcch = BTCChinaTicker(self)

    bpcad = BitpayTicker(self, 'CAD')
    bpusd = BitpayTicker(self, 'USD')
    bpgbp = BitpayTicker(self, 'GBP')
    bpeur = BitpayTicker(self, 'EUR')

    self.p_boardlets = [ \
      [ van,            nyt,            lot,            frk,            bet            ] ,
      [ usdcad,         kr_usd,         usdgbp,         usdeur,         usdcny         ] ,
      [ qu_ca,          qu_us,          cd_gbp,         cd_eur,         cd_cny         ] ,
      [ cbcad,          cbusd,          cbgbp,          cbeur,          btcch          ] ,
      [ bpcad,          bpusd,          bpgbp,          bpeur,          btstmp         ] ]

    grid = QtGui.QGridLayout()

    for row in range(0, len(self.p_boardlets)):
      for col in range(0, len(self.p_boardlets[0])):
        grid.addWidget(self.p_boardlets[row][col], row, col)

    self.setLayout( grid )
    self.showMaximized()

  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape or e.key() == QtCore.Qt.Key_Q:
      self.close()

