from xml.sax import make_parser
from plugin import VarselParser, format_weather

varselxml = urlopen('http://www.yr.no/sted/Norge/Oslo/Oslo/Oslo/forecast.xml')
parser = make_parser()
parser.setFeature(feature_namespaces, False)
parser.setFeature(feature_validation, False)
dh = VarselParser()
parser.setContentHandler(dh)
try:
    parser.parse(varselxml)
except SAXException, e:
    print e

item = dh.items[0]

text = format_weather(item)

print text

