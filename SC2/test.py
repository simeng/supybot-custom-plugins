from urllib2 import urlopen
import json

#d = urlopen("http://sc2ranks.com/api/char/eu/Yggdar$658").read()
d = open("dump").read()

js = json.loads(d)

bnet_id = unicode(js['bnet_id'])
for t in js['teams']:
    print "[%sv%s] %s/%s [%s] %3spt %s #%s" % ( t['bracket'], t['bracket'], t['wins'], t['losses'], t['league'], t['points'], t['division'], t['division_rank'] )

