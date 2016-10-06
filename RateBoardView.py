#!/usr/bin/python
# -*- coding: utf-8 -*-

import datetime
import os
import random
import sys

from PyQt4 import QtGui,QtCore

from boardlet import Boardlet
from clockboardlet import ClockBoardlet
from forexticker import ForexTicker
from goldticker import GoldTicker
from coindeskbpiticker import CoindeskBPITicker
from krakenticker import KrakenTicker
from bitstampticker import BitstampTicker
from cexioticker import CEXIOTicker
from coinbaseticker import CoinbaseTicker
from btcchinaticker import BTCChinaTicker
from bitpayticker import BitpayTicker
from quadrigaticker import QuadrigaTicker
from taurusticker import TaurusTicker
from myticker import MyTicker

def go():
  app = QtGui.QApplication(sys.argv)
  mw = MainWindow()
  sys.exit(app.exec_())

class MainWindow(QtGui.QWidget):
  def __init__(self):
    super(MainWindow, self).__init__()
    self.initUI()

  def initUI(self):
    # custom list of color names for different background gradients
    self.p_colorIndex = 0
    self.p_colors = [ QtGui.QColor("red"),
                      QtGui.QColor("darkRed"),
                      QtGui.QColor("green"),
                      QtGui.QColor("darkGreen"),
                      QtGui.QColor("blue"),
                      QtGui.QColor("darkBlue"),
                      QtGui.QColor("cyan"),
                      QtGui.QColor("darkCyan"),
                      QtGui.QColor("darkMagenta"),
                      QtGui.QColor(153,153,0),
                      QtGui.QColor(51,51,0) ]

    self.setWindowTitle( 'Rate Board - ' +
                         datetime.datetime.now().strftime("%d %b %H:%M") )
    self.setWindowIcon( QtGui.QIcon(os.getcwd() + "/img/my.png") )

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
    qu_ca = QuadrigaTicker( self, 'CAD' )
    btstmp = BitstampTicker( self )

    tacad = TaurusTicker(self, 'CAD')
    cbusd = CoinbaseTicker(self, 'USD')
    cbgbp = CoinbaseTicker(self, 'GBP')
    cbeur = CoinbaseTicker(self, 'EUR')

    btcch = BTCChinaTicker(self)

    krcad = KrakenTicker(self, 'CAD')

    xauusd = GoldTicker(self)
    bpgbp = BitpayTicker(self, 'GBP')
    bpeur = BitpayTicker(self, 'EUR')

    my_us = MyTicker(self, kr_usd.p_model, cbusd.p_model )

    self.p_boardlets = [ \
      [ van,    nyt,    lot,    frk,    bet    ] ,
      [ usdcad, kr_usd, usdgbp, usdeur, usdcny ] ,
      [ qu_ca,  my_us,  cd_gbp, cd_eur, cd_cny ] ,
      [ tacad,  cbusd,  cbgbp,  cbeur,  btcch  ] ,
      [ krcad,  xauusd, bpgbp,  bpeur,  btstmp ] ]

    grid = QtGui.QGridLayout()

    for row in range(0, len(self.p_boardlets)):
      for col in range(0, len(self.p_boardlets[0])):
        grid.addWidget(self.p_boardlets[row][col], row, col)

    self.setLayout( grid )
    self.showMaximized()

    # set up a timer to do a repaint every so often from the ui thread
    self.startTimer( 30 * 1000 ) # 30 seconds, in msec

  def keyPressEvent(self, e):
    if e.key() == QtCore.Qt.Key_Escape or e.key() == QtCore.Qt.Key_Q:
      self.close()

    if e.key() == QtCore.Qt.Key_R:
      # force background update for testing
      self.makeBackground()
      self.update()

  def timerEvent(self, e):
    # only make a new background on average every 20th timeout
    if random.random() < 0.05:
      self.makeBackground()

    self.repaint()

  def makeBackground(self):
    nextColor = self.p_colors[self.p_colorIndex]
    if self.p_colorIndex < len(self.p_colors) - 1:
      self.p_colorIndex = self.p_colorIndex + 1
    else:
      self.p_colorIndex = 0

    pal = QtGui.QPalette()
    gradient = QtGui.QLinearGradient(0, 0, 0, self.frameGeometry().height())
    gradient.setColorAt(0.0, QtGui.QColor(0, 0, 0))
    gradient.setColorAt(1.0, nextColor)
    pal.setBrush(QtGui.QPalette.Window, QtGui.QBrush(gradient))
    self.setPalette( pal )

