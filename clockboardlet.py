#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
from PyQt4 import QtGui,QtCore

import datetime
import time

from boardlet import Boardlet

class ClockBoardlet(Boardlet):
  def __init__(self, parent, city):
    super(ClockBoardlet, self).__init__(parent)
    self.p_city = city
    self.initUI()

  def initUI(self):
    super(ClockBoardlet, self).initUI()
    self.p_icon = QtGui.QLabel(self)
    self.p_icon.setGeometry(20,20,60,60)
    self.p_icon.setPixmap( QtGui.QPixmap(os.getcwd() + '/worldclock.png') )

  def paintEvent(self, e):
    super(ClockBoardlet, self).paintEvent(e)

    tnow = '--:--'
    fdat = 'Sun, 01 Jan'
    tz = '+00:00'
    ct = None

    if self.p_city == 'London':
      ct = LondonTime()
    if self.p_city == 'New York':
      ct = NewYorkTime()
    if self.p_city == 'Beijing':
      ct = BeijingTime()
    if self.p_city == 'Frankfurt':
      ct = FrankfurtTime()
    if self.p_city == 'Vancouver':
      ct = VancouverTime()

    tnow = ct.time()
    tz = ct.tzadj()
    fday = ct.day()

    qp = QtGui.QPainter()
    qp.begin(self)

    qp.setPen( self.p_grayPen )
    qp.setFont( self.p_pairFont )
    qp.drawText( 85, 32, self.p_city )

    qp.setPen( self.p_whitePen )
    qp.setFont( self.p_rateFont )
    qp.drawText( 85, 60, tnow )

    qp.setFont( self.p_pairFont )
    qp.drawText( 175, 60, fday )
    qp.setPen( self.p_grayPen )
    qp.drawText( 85, 79, tz )

    qp.end()

# ------------------------------------------------------------------------------------------
# Following are timezone classes - Python does not provide default implementation for tzinfo
# ------------------------------------------------------------------------------------------
class EDT(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=-4)
  def dst(self, dt):
    return datetime.timedelta(0)

class EST(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=-5)
  def dst(self, dt):
    return datetime.timedelta(0)

# GMT == Standard Time in Britain
class GMT(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=1)
  def dst(self, dt):
    return datetime.timedelta(0)

# British Summer Time == DST in Britain
class BST(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=1)
  def dst(self, dt):
    return datetime.timedelta(0)

# China Standard Time (no DST)
class CST(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=+8)
  def dst(self, dt):
    return datetime.timedelta(0)

# Central European Summer Time
class CEST(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=2)
  def dst(self, dt):
    return datetime.timedelta(0)

# Central European Time
class CET(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=1)
  def dst(self, dt):
    return datetime.timedelta(0);

class PDT(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=-7)
  def dst(self, dt):
    return datetime.timedelta(0);

class PST(datetime.tzinfo):
  def utcoffset(self, dt):
    return datetime.timedelta(hours=-8)
  def dst(self, dt):
    return datetime.timedelta(0);

# --------------------------------------------------------------------------------------------
# Following are city-specific classes that are DST-sensitive, return formatted strings
# --------------------------------------------------------------------------------------------
class TimeBase(object):
  def __init__(self):
    self.p_datetime = datetime.datetime.now()

  def tzadj(self):
    return self.p_datetime.strftime('%z')

  def day(self):
    return self.p_datetime.strftime('%a, %d %b')

  def formattedTime(self):
    return self.p_datetime.strftime('%H:%M')

class LondonTime(TimeBase):
  def __init__(self):
    super(LondonTime, self).__init__()

  def time(self):
    if time.daylight:
      self.p_datetime = datetime.datetime.now(BST())
    else:
      self.p_datetime = datetime.dateime.now(GMT())
    return self.formattedTime()

class NewYorkTime(TimeBase):
  def __init__(self):
    super(NewYorkTime, self).__init__()

  def time(self):
    self.p_datetime = datetime.datetime.now()
    if time.daylight:
      self.p_datetime = datetime.datetime.now(EDT())
    else:
      self.p_datetime = datetime.dateime.now(EST())
    return self.formattedTime()

class BeijingTime(TimeBase):
  def __init__(self):
    super(BeijingTime, self).__init__()
    self.p_datetime = datetime.datetime.now(CST())

  def time(self):
    return self.formattedTime()

class FrankfurtTime(TimeBase):
  def __init__(self):
    super(FrankfurtTime, self).__init__()

  def time(self):
    self.p_datetime = datetime.datetime.now()
    if time.daylight:
      self.p_datetime = datetime.datetime.now(CEST())
    else:
      self.p_datetime = datetime.dateime.now(CET())
    return self.formattedTime()

class VancouverTime(TimeBase):
  def __init__(self):
    super(VancouverTime, self).__init__()

  def time(self):
    self.p_datetime = datetime.datetime.now()
    if time.daylight:
      self.p_datetime = datetime.datetime.now(PDT())
    else:
      self.p_datetime = datetime.dateime.now(PST())
    return self.formattedTime()

# ----------
# Test code
# ----------
def main( argv=None ):
  lon = LondonTime()
  print 'time in London:', lon.time()

  nyc = NewYorkTime()
  print 'time in NYC:', nyc.time()

  bei = BeijingTime()
  print 'time in Beijing:', bei.time()

if __name__ == '__main__':
    main()
