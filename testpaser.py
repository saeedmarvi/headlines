# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 16:39:44 2017

@author: 5004756
"""

import urllib2, feedparser
proxy = urllib2.ProxyHandler( {"http":"http://internet.proxy.fedex.com:3128", \
                               "https":"https://internet.proxy.fedex.com:3128"} )


d = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml')
if 'bozo_exception' in d.keys():
    d = feedparser.parse('http://feeds.bbci.co.uk/news/rss.xml',handlers=[proxy])
    
