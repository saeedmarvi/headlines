# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a python script file.
"""
import urllib2, feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640'}

PROXY = urllib2.ProxyHandler( {"http":"http://internet.proxy.fedex.com:3128", \
                               "https":"https://internet.proxy.fedex.com:3128"} )

@app.route("/")
#In Flask, if we specify a part of our URL path in angle brackets < >, 
# then it is taken as a variable and is passed to our application code. 
#@app.route("/<publication>")

def get_news():
    # get the user input of publication query and do the check
    query = request.args.get("publication")
    if not query or query.lower() not in RSS_FEEDS:
        publication = "bbc"
    else:
        publication = query.lower()
    # get the feed without proxy if get error, then use proxy
    feed = feedparser.parse(RSS_FEEDS[publication])
    # if find some error
    if 'bozo_exception' in feed.keys():
        feed = feedparser.parse(RSS_FEEDS[publication], handlers = [PROXY])
        
#    first_article = feed['entries'][0]
    return render_template("home.html",\
                           feedsource = publication.upper(),
                           articles=feed['entries'])
# =============================================================================
#     return """<html>
#       <body>
#         <h1> News Headlines </h1>
#         <b>{0}</b> <br/>
#         <i>{1}</i> <br/>
#         <p>{2}</p> <br/>
#       </body>
#      </html>""".format(first_article.get("title"), first_article.get("published"), first_article.get("summary"))
# 
# =============================================================================

if __name__ == '__main__':
    app.run(port=5000, debug=True)