
# Copyright (c) 2008, emh
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
#   * Redistributions of source code must retain the above copyright notice,
#     this list of conditions, and the following disclaimer.
#   * Redistributions in binary form must reproduce the above copyright notice,
#     this list of conditions, and the following disclaimer in the
#     documentation and/or other materials provided with the distribution.
#   * Neither the name of the author of this software nor the name of
#     contributors to this software may be used to endorse or promote products
#     derived from this software without specific prior written consent.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED.  IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

###

'''
lookup norwegian phone numbers
'''

import supybot.utils as utils
#from supybot.commands import *
from supybot import commands
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs

#sys.path.insert('/home/alexis/plugins/WTF8')
import BeautifulSoup, sys, re, urllib

class AttenNittiParser:
    def __init__(self):
        self.soup = BeautifulSoup.BeautifulSoup()

    def lookup(self, tlf):
        """ Lookup using http get variables contained in data """
        url = "http://1890.no/?type=Privat&query=%d" % tlf
        data = urllib.urlopen(url).read()

        self.soup.feed(data.decode("UTF-8"))
        interesting_row = self.soup.find(attrs={"class": re.compile(".*vcard.*")})

        data = dict([(x.attrs[0][1], x.text) for x in interesting_row.findAll("span") ])
        return data
        

class Tlf(callbacks.Plugin):
    """Add the help for "@plugin help Tlf" here
    This should describe *how* to use this plugin."""

    def tlf(self, irc, msg, args, opts, lookup):
        '''
        <tlf number>
        '''

        parser = AttenNittiParser()
        data = parser.lookup(int(lookup))
        reply = ', '.join([ "%s: %s" % (k.encode("UTF-8"), v.encode("UTF-8")) for k, v in data.items() ])
        if reply:
            irc.reply(reply, prefixNick=False)

    tlf = commands.wrap(tlf, [commands.getopts({}), 'text'])

Class = Tlf


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
