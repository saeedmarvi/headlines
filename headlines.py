# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a python script file.
"""
import feedparser
from flask import Flask
from flask import render_template # render the html template
from flask import request #import flask's request context

import json
import urllib2
import urllib

import datetime # to set lifespan of soon-to-exist cookies
from flask import make_response # to create a response object tht we can set cookies on

app = Flask(__name__)

RSS_FEEDS = {'BBC': 'http://feeds.bbci.co.uk/news/rss.xml',
             'CNN': 'http://rss.cnn.com/rss/edition.rss',
             'FOX': 'http://feeds.foxnews.com/foxnews/latest',
             'WSJ': 'http://www.wsj.com/xml/rss/3_7085.xml'}
# global weather url
WEATHER_URL='http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=0bff3c74105bdee3dd2d5db4e5548eab'
# global currency url
CURRENCY_URL = "https://openexchangerates.org//api/latest.json?app_id=e54adb9ea8904e218cf05ca7a6fbb5e3"

# =============================================================================
# PROXY = urllib2.ProxyHandler( {"http":"http://internet.proxy.fedex.com:3128", \
#                                "https":"https://internet.proxy.fedex.com:3128"} )
# =============================================================================

# default values
DEFAULTS = {'publication':'BBC',
            'city': 'Memphis, US',
            'currency_from':'USD',
            'currency_to':'CNY'}

# get key values
def get_value_with_fallback(key):
    if request.args.get(key):
        return request.args.get(key)
    if request.cookies.get(key):
        return request.cookies.get(key)
    return DEFAULTS[key]


@app.route("/")

def home():
    #get customized headlines, based on user input or default
    publication = get_value_with_fallback("publication")
    articles = get_news(publication.upper())
    
    #get customized weather, based on user input or default
    city = get_value_with_fallback("city")
    weather = get_weather(city)
    
    #get customeized currency, based on user input
    currency_from = get_value_with_fallback("currency_from")
    currency_to = get_value_with_fallback("currency_to")
    rate, currencies = get_rate(currency_from, currency_to)
    # render template and return
# =============================================================================
#     return render_template("index.html", publication=publication.upper(), 
#                                          articles=articles, 
#                                          weather=weather,
#                                          currency_from=currency_from,
#                                          currency_to=currency_to,
#                                          rate=rate,
#                                          currencies=currencies)
# =============================================================================
    response = make_response(render_template("index.html",
                                             publication=publication.upper(),
                                             publications=RSS_FEEDS.keys(),
                                             articles=articles,
                                             weather=weather,
                                             currency_from=currency_from,
                                             currency_to=currency_to,
                                             rate=rate,
                                             currencies=sorted(currencies)))
    expires = datetime.datetime.now() + datetime.timedelta(days=365)
    response.set_cookie("publication", publication, expires=expires)
    response.set_cookie("city", city, expires=expires)
    response.set_cookie("currency_from", currency_from, expires=expires)
    response.set_cookie("currency_to", currency_to, expires=expires)
    return response

def get_news(pub):
    if not pub or pub not in RSS_FEEDS:
        pub = DEFAULTS['publication']
    # get the news feed using RSS feeds    
    feed = feedparser.parse(RSS_FEEDS[pub])
    return feed['entries']

def get_weather(city):
    ###### keep if behind proxy, otherwise, don't use 
# =============================================================================
#     if len(urllib2.getproxies()) > 0:
#         opener = urllib2.build_opener(PROXY)
#         urllib2.install_opener(opener)
# =============================================================================
    
    # We use urllib.quote() on the query city variable, as URLs cannot have spaces in them, 
    # but the names of the cities that we want to retrieve weather for may contain spaces. 
    # The quote() function handles this for us by, for example, translating a space to "%20",
    # which is how spaces are represented in URLs. 
    query = urllib.quote(city)
    # combine the query city into the url
    url = WEATHER_URL.format(query)
    # read the response data
    data = urllib2.urlopen(url).read()
    # parse into json object
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description":parsed["weather"][0]["description"],
                   "temperature":parsed["main"]["temp"],
                   "city":parsed["name"],
                   "country":parsed['sys']['country']}
    return weather


def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENCY_URL).read()
    
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate/frm_rate,parsed.keys())

if __name__ == '__main__':
  app.run(port=5000, debug=True)