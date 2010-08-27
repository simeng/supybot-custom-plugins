###
###

import supybot.utils as utils
from supybot.commands import *
import supybot.callbacks as callbacks
import sys
import sgmllib
import urllib
from BeautifulSoup import BeautifulSoup, BeautifulStoneSoup

class Posten(callbacks.Plugin):
    def __init__(self, irc):
        callbacks.Plugin.__init__(self, irc)
        self.status_format = u'%(date)s: %(status)s %(location)s'
        self.package_format = u'[%s] %s'
        self.packageStates = {}
        self.errorReported = False

    def pakke(self, irc, msg, args, opts, packageId):
        """[--all] [--once] <packageId>

        Show latest movements of a package
        """

        try:
            packagehtml = urllib.urlopen("http://sporing.posten.no/sporing.html?q=%s" % packageId).read()
            #packagehtml = open("plugins/Posten/dump", "r").read()
        except IOError, i:
            if self.errorReported == False and opts[0][0] == 'once':
                irc.reply("Posten.no seems down when checking packageId %s" % packageId)
            self.errorReported = True
            return

        self.errorReported = False

        data = self.parse(packagehtml)

        if len(data) > 0:
            string = u''
            if opts:
                if opts[0][0] == 'all':
                    for pkg in data:
                        string += self.package_format % (pkg["id"], u', '.join([self.status_format % (x) for x in pkg["statuses"]])) + " "
                else:
                    for pkg in data:
                        string += self.package_format % (pkg["id"], self.status_format % (pkg["statuses"][0])) + " "


                if opts[0][0] == 'once':
                    if self.packageStates.has_key(packageId):
                        if string == self.packageStates[packageId]:
                            return
            if not string:
                for pkg in data:
                    string += self.package_format % (pkg["id"], self.status_format % (pkg["statuses"][0]))
            self.packageStates[packageId] = string
            irc.reply(string.encode("UTF-8"))


    def parse(self, data):
        soup = BeautifulSoup(data, convertEntities=BeautifulStoneSoup.HTML_ENTITIES)

        track_tbl = soup.findAll("li", {"class":"sporing-sendingandkolli-kolli-details"})

        packages = []
        for package in track_tbl:
            if not package.find("span"):
                id = 'pkg'
            else:
                id = package.find("span").string.strip(),
            pkg = {
                'id': id,
                'statuses': []
            }

            events = package.findAll("tr")
            for event in events:
                cols = event.findAll("td")
                if len(cols) == 3:
                    d = {}
                    status = cols[0].div.contents[0]
                    if len(cols[0].div.contents) > 1:
                        if cols[0].div.contents[1]:
                            status += cols[0].div.contents[1].string
                        else:
                            status += cols[0].div.contents[1][0].string
                        status += cols[0].div.contents[2]
                    d['date'] = cols[1].string.strip()
                    d['status'] = status.strip()
                    d['location'] = cols[2].string.strip()
                    pkg["statuses"].append(d)

            packages.append(pkg)
        return packages


    pakke = wrap(pakke, [getopts({'all':'', 'once':''}),'text'])


Class = Posten

