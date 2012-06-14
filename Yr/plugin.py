#
# -*- coding: UTF-8 -*
### (C) Lart Inc

import supybot.utils as utils
from supybot.commands import *
import supybot.callbacks as callbacks

import sys
import sgmllib
from urllib2 import urlopen
from urllib import quote
from xml.sax import ContentHandler
from xml.sax import make_parser
from xml.sax import saxutils
from xml.sax import SAXException
from xml.sax.handler import feature_namespaces
from xml.sax.handler import feature_validation
import re
import time

def normalize_whitespace(text):
    "Remove redundant whitespace from a string"
    return ' '.join(text.split())

def format_weather(item):
    if item['temperature']['unit'] == 'celsius':
        temptype = 'C'
    else:
        temptype = 'F'

    return u'%s: %s, %d°%s, %s %.1fm/s %s' % (
            item['station']['name'],
            item['symbol']['name'],
            int(item['temperature']['value']),
            temptype,
            item['wind']['speed']['name'],
            float(item['wind']['speed']['mps']),
            item['wind']['direction']['name']
    )

class Yr(callbacks.Plugin):
    def __init__(self, irc):
        callbacks.Plugin.__init__(self, irc)

    def varsel(self, irc, msg, args, opts, verargs):
        """[--all] <sted>

        Les mer om vilkår for bruk av gratis værdata + retningslinjer på http://www.yr.no/verdata/ 
        """
       
        place = verargs.capitalize()
        viktigestader = file('plugins/Yr/places.txt').read()
        pattern = '[0-9]+\t%s\t[0-9]+.*\thttp://(?P<url>.*)\t' % place
        url = re.findall(pattern, viktigestader)

        if not url:
            irc.reply(u'Kjenner ikke til stedet %s.'.encode('UTF-8') % place)
            return

        url = url[0]
        url = quote(url)
        varselxml = urlopen('http://' + url)

        parser = make_parser()
        parser.setFeature(feature_namespaces, False)
        parser.setFeature(feature_validation, False)
        dh = VarselParser()
        parser.setContentHandler(dh)
        try:
            parser.parse(varselxml)
        except SAXException:
            irc.reply('Parse Exception')

        item = dh.items[0]

        text = format_weather(item)

        irc.reply(text.encode('UTF-8'))

    varsel = wrap(varsel, [getopts({'all':''}),'text'])

Class = Yr

class VarselParser(ContentHandler):

    def __init__(self):
        self.inBodyContent = False
        self.done = False
        self.item = {}
        self.items = []

    def startElement(self, name, attrs):
        if name == 'weatherstation': 
            self.item['station'] = dict(attrs.items())
        if name == 'symbol': 
            self.item['symbol'] = dict(attrs.items())
        if name == 'temperature': 
            self.item['temperature'] = dict(attrs.items())
        if name == 'windDirection': 
            if not 'wind' in self.item.keys():
                self.item['wind'] = {}
            self.item['wind']['direction'] = dict(attrs.items())
        if name == 'windSpeed': 
            if not 'wind' in self.item:
                self.item['wind'] = {}
            self.item['wind']['speed'] = dict(attrs.items())

    def endElement(self, name):
        if name == 'weatherstation':
            self.items.append(self.item)
            self.item = {}

        if name == 'observations':
            self.done = True

