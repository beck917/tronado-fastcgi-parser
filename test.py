#!/usr/bin/env python
"""
<description>

"""

__author__="Beck Xu"
__date__ ="$2012-8-19 16:19:38$"

from php.fpm import PHPFPM

if __name__ == "__main__":
    
    fpm = PHPFPM()
    print fpm
    tmp = fpm.get()
    print tmp
    
    print "Hello World"
