#!/usr/bin/env python
"""
<description>

This file is part of ZTC and distributed under the same license.
http://bitbucket.org/rvs/ztc/

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import time

import libs.fcgi_app as fcgi_client

class PHPFPM():
    name = "php-fpm"
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 2
    
    def __init__(self, name=None):
        self.fcgi_port = 9000
        self.fcgi_host = '127.0.0.1'
        
    def _load_page(self, url):
        """ load fastcgi page """
        try:
            fcgi = fcgi_client.FCGIApp(host = self.fcgi_host,
                                       port = self.fcgi_port)
            env = {
               'SCRIPT_FILENAME': "/var/www%s" % url,
               'QUERY_STRING': '',
               'REQUEST_METHOD': 'GET',
               'SCRIPT_NAME': url,
               'REQUEST_URI': url,
               'GATEWAY_INTERFACE': 'CGI/1.1',
               'SERVER_SOFTWARE': 'ztc',
               'REDIRECT_STATUS': '200',
               'CONTENT_TYPE': '',
               'CONTENT_LENGTH': '0',
               'DOCUMENT_URI': url,
               'DOCUMENT_ROOT': '/var/www',
               'SERVER_PROTOCOL' : 'HTTP/1.1',
               'REMOTE_ADDR': '127.0.0.1',
               'REMOTE_PORT': '123',
               'SERVER_ADDR': self.fcgi_host,
               'SERVER_PORT': str(self.fcgi_port),
               'SERVER_NAME': self.fcgi_host
               }
            ret = fcgi(env)
            return ret
        except:
            return '500', [], '', ''

    def get(self):
        """ calls php-fpm ping resource """
        st = time.time()
        code, headers, out, err = self._load_page('/ping.php')
        print code
        print err
        print out
        print time.time() - st
        if code.startswith('200') and out == 'pong':
            print out
            print time.time() - st
            return out
        else:
            return 0