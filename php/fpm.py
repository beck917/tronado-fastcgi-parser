#!/usr/bin/env python
"""
<description>

This file is part of ZTC and distributed under the same license.
http://bitbucket.org/rvs/ztc/

Copyright (c) 2011 Vladimir Rusinov <vladimir@greenmice.info>
"""

import time

from libs.check import ZTCCheck, CheckFail
import libs.fcgi_app as fcgi_client

class PHPFPMCheck(ZTCCheck):
    name = "php-fpm"
    
    OPTPARSE_MIN_NUMBER_OF_ARGS = 1
    OPTPARSE_MAX_NUMBER_OF_ARGS = 2
    
    def _myinit(self):
        self.fcgi_port = self.config.get('fpm_port', 9000)
        self.fcgi_host = self.config.get('fpm_host', '127.0.0.1')
    
    def _get(self, metric, *arg, **kwarg):
        if metric == 'ping':
            return self.ping
        elif metric == 'status':
            m = arg[0]
            return self.get_status(m)
        else:
            raise CheckFail("uncknown metric")
        
    def _load_page(self, url):
        """ load fastcgi page """
        try:
            fcgi = fcgi_client.FCGIApp(host = self.fcgi_host,
                                       port = self.fcgi_port)
            env = {
               'SCRIPT_FILENAME': url,
               'QUERY_STRING': '',
               'REQUEST_METHOD': 'GET',
               'SCRIPT_NAME': url,
               'REQUEST_URI': url,
               'GATEWAY_INTERFACE': 'CGI/1.1',
               'SERVER_SOFTWARE': 'ztc',
               'REDIRECT_STATUS': '200',
               'CONTENT_TYPE': '',
               'CONTENT_LENGTH': '0',
               #'DOCUMENT_URI': url,
               'DOCUMENT_ROOT': '/',
               'DOCUMENT_ROOT': '/var/www/',
               #'SERVER_PROTOCOL' : ???
               'REMOTE_ADDR': '127.0.0.1',
               'REMOTE_PORT': '123',
               'SERVER_ADDR': self.fcgi_host,
               'SERVER_PORT': str(self.fcgi_port),
               'SERVER_NAME': self.fcgi_host
               }
            ret = fcgi(env)
            return ret
        except:
            self.logger.exception('fastcgi load failed')
            return '500', [], '', ''
        
        
    @property
    def ping(self):
        """ calls php-fpm ping resource """
        st = time.time()
        code, headers, out, err = self._load_page('/ping')
        if code.startswith('200') and out == 'pong':
            return time.time() - st
        else:
            self.logger.error('ping: got response, but not correct')
            return 0
    
    def get_status(self, metric):
        """ get php-fpm status metric """
        metric = metric.replace('_', ' ')
        
        page = self.get_status_page()
        if not page:
            raise CheckFail("unable to get status page")
        for line in page.splitlines():
            if line.startswith(metric):
                return line.split()[-1]
        # no such metric found
        raise CheckFail("no such metric found")
            
    
    def get_status_page(self):
        """ return php-ftm status page text """
        code, headers, out, err = self._load_page('/status')
        if code.startswith('200'):
            return out
        else:
            self.logger.error('ping: got response, but not correct')
            return None                