# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a python script file.
"""
import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib2
import urllib

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'wsj': 'http://www.wsj.com/xml/rss/3_7085.xml'}

PROXY = urllib2.ProxyHandler( {"http":"http://internet.proxy.fedex.com:3128", \
                               "https":"https://internet.proxy.fedex.com:3128"} )

DEFAULTS = {'publication':'bbc',
            'city':'Memphis, USA',
            'currency_from': 'USD',
            'currency_to':'CNY'}
WEATHER_URL = 'http://api.openweathermap.org/data/2.5/weather?q={0}&units=metric&appid=cb932829eacb6a0e9ee4f38bfbf112ed'
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=e54adb9ea8904e218cf05ca7a6fbb5e3"

@app.route("/")
#In Flask, if we specify a part of our URL path in angle brackets < >, 
# then it is taken as a variable and is passed to our application code. 
#@app.route("/<publication>")
def home():
    # get customized weather based on user input or default
    city = request.args.get("city")
    if not city:
        city = DEFAULTS['city']
    # call get_weather function to get the weather
    weather = get_weather(city)
    
    # get customized news feeds, based on user input news resource or default
    publication = request.args.get("publication")
    if not publication or publication.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    
    #get customized currency from based on user input or default
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    
    currency_to = request.args.get("currency_to")
    if not currency_to:
        currency_to = DEFAULTS["currency_to"]
    rate, currencies = get_rate(currency_from, currency_to)
    # reder template
    return render_template("home.html",
                           feedsource = publication.upper(),
                           articles=articles,
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate=rate,
                           currencies=sorted(currencies))
    

def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS["publication"]
    else:
        publication = query.lower()    
    # get the feed without proxy if get error, then use proxy
    feed = feedparser.parse(RSS_FEEDS[publication])
    # if find some error
    if 'bozo_exception' in feed.keys():
        feed = feedparser.parse(RSS_FEEDS[publication], handlers = [PROXY])
        
#    first_article = feed['entries'][0]
    return feed['entries']
    
    
def get_weather(query):
    ###### keep if behind proxy, don't use otherwise
    if len(urllib2.getproxies()) > 0:
        opener = urllib2.build_opener(PROXY)
        urllib2.install_opener(opener)
   
    # prepare url
    query = urllib.quote(query)
    url = WEATHER_URL.format(query)
    
    #get the response data and parse
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    # extract weather info
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],\
                   "temperature":parsed["main"]["temp"],\
                   "city":parsed["name"],
                   'country': parsed['sys']['country']
                  }
    return weather

def get_rate(frm, to):
    ###### keep if behind proxy, don't use otherwise
    if len(urllib2.getproxies()) > 0:
        opener = urllib2.build_opener(PROXY)
        urllib2.install_opener(opener)
        
    ## get all currency
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate, parsed.keys())

if __name__ == '__main__':
    app.run(port=5000, debug=True)