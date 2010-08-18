import supybot.utils as utils
from supybot.commands import *
import supybot.callbacks as callbacks
import sys
import urllib
import json

class SC2(callbacks.Plugin):
    def __init__(self, irc):
        callbacks.Plugin.__init__(self, irc)
        self.errorReported = False

    def sc(self, irc, msg, args, name, bnet_id):
        """<name> [<bnet_id>]

        Show sc2 ranks for a character
        """

        colors = range(3, 16)

        if bnet_id == None:
            try:
                url = "http://sc2ranks.com/api/search/eu/%s" % (name)
                d = urllib.urlopen(url).read()
            except IOError, i:
                irc.reply("Failed searching for character %s" % (name))
                return

            js = json.loads(d)

            if js['total'] == 0:
                irc.reply("Didn't find anyone named '%s'" % (name))
                return
            elif js['total'] == 1:
                bnet_id = unicode(js['characters'][0]['bnet_id'])
                name = js['characters'][0]['name']
            else:
                irc.reply("Found the following bnet_ids: " + ", ".join(["%s[%s]" % (char['name'], unicode(char['bnet_id'])) for char in js['characters']]))
                return

        try:
            url = "http://sc2ranks.com/api/char/eu/%s!%s" % (name, bnet_id)
            d = urllib.urlopen(url).read()
        except IOError, i:
            if self.errorReported == False:
                irc.reply("SC2Ranks.com seems to be down checking for %s" % (url))
            self.errorReported = True
            return

        self.errorReported = False

        js = json.loads(d)

        if len(js) > 0:
            string = u''
            
            bnet_id = unicode(js['bnet_id'])
            string += 'http://eu.battle.net/sc2/en/profile/%s/1/%s/ ' % (bnet_id, name)
            i = 0
            for t in js['teams']:
                string += "\x03%s" % ( colors[t['bracket']] )
                string += "[%sv%s] %s/%s [%s] %spt %s #%s  " % ( t['bracket'], t['bracket'], t['wins'], t['losses'], t['league'], t['points'], t['division'], t['division_rank'] )
                string += "\x03"
                i +=1

            irc.reply(string.encode("UTF-8"))

    sc = wrap(sc, ['something', optional('something')])


Class = SC2

