# -*- coding: utf-8 -*-
"""
Created on Mon Sep 25 23:01:13 2017

@author: 5004756
"""

import json
import urllib2
import urllib

# keep if behind proxy, delete otherwise
proxy = urllib2.ProxyHandler( {"http":"http://internet.proxy.fedex.com:3128", \
                               "https":"https://internet.proxy.fedex.com:3128"} )
#opener = urllib2.build_opener(proxy)
#urllib2.install_opener(opener)
#
## keep no matter behind proxy or not
#api_url = 'http://api.openweathermap.org/data/2.5/weather?q=London,uk&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
#data = urllib2.urlopen(api_url).read()
#
## parse json data
#parsed = json.loads(data)
#
#weather = None
#if parsed.get("weather"):
#    weather = {"description":parsed["weather"][0]["description"],\
#               "temperature":parsed["main"]["temp"],\
#               "city":parsed["name"]
#                  }
#print weather



def get_weather(query):
    # keep if behind proxy, delete otherwise
    opener = urllib2.build_opener(proxy)
    urllib2.install_opener(opener)
    
    # prepare url
    api_url = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
    query = urllib.quote(query)
    print query
    url = api_url.format(query)
    print url
    #get the response data and parse
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    # extract weather info
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],\
                   "temperature":parsed["main"]["temp"],\
                   "city":parsed["name"]
                  }
        return weather
    
    
w = get_weather("London, UK")
print w