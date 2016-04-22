#!/usr/bin/python
# -*- coding: utf-8 -*-

import time

class Modellet(object):
  def __init__(self):
    self.p_refreshTime = None
    self.p_fault = True

  def getLastUpdated(self):
    if None == self.p_refreshTime:
      return 'dd Mon 00:00Z'
    return time.strftime('%d %b %H:%MZ', self.p_refreshTime)

  def setLastUpdatedNow(self):
    self.p_refreshTime = time.gmtime()

  def getFaultFlag(self):
    return self.p_fault

  def setFaultFlag(self,newval):
    self.p_fault = newval

