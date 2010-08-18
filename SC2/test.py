from urllib2 import urlopen
import json
import sys

#d = urlopen("http://sc2ranks.com/api/search/eu/Yggdar").read()
d = open("dumpsearch").read()
js = json.loads(d)

print js['total']
if js['total'] == 0:
    print "Not found"
elif js['total'] == 1:
    print unicode(js['characters'][0]['bnet_id'])
else:
    print ", ".join(["%s[%s]" % (char['name'], unicode(char['bnet_id'])) for char in js['characters']])

sys.exit()


#d = urlopen("http://sc2ranks.com/api/char/eu/Yggdar$658").read()
d = open("dump").read()

js = json.loads(d)

bnet_id = unicode(js['bnet_id'])
for t in js['teams']:
    print "[%sv%s] %s/%s [%s] %3spt %s #%s" % ( t['bracket'], t['bracket'], t['wins'], t['losses'], t['league'], t['points'], t['division'], t['division_rank'] )

