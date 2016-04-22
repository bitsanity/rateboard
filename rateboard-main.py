#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import RateBoardView

def main():
    if None == os.getenv( 'DISPLAY' ):
      os.putenv( 'DISPLAY', ':2.0' )

    RateBoardView.go()

if __name__ == '__main__':
    main()

