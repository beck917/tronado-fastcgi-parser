#!/usr/bin/env python
"""
<description>

"""

__author__="Beck Xu"
__date__ ="$2012-8-19 16:19:38$"

from php.fpm import PHPFPMCheck

if __name__ == "__main__":
    
    fpm = PHPFPMCheck()
    print fpm
    tmp = fpm.ping()
    print tmp
    
    print "Hello World"
