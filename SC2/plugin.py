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

    def sc(self, irc, msg, args, name, charcode):
        """<name> <charcode>

        Show sc2 ranks for a character
        """

        colors = range(3, 16)

        try:
            url = "http://sc2ranks.com/api/char/eu/%s$%s" % (name, charcode)
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

    sc = wrap(sc, ['something', 'something'])


Class = SC2

