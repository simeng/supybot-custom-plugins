
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

import urllib2
import re
import sys

class Tlf(callbacks.Plugin):
    """Add the help for "@plugin help Tlf" here
    This should describe *how* to use this plugin."""

    def tlf(self, irc, msg, args, opts, lookup):
        '''
        <tlf number>
        '''

        f = urllib2.urlopen("http://www.1881.no/?Query=" + urllib2.quote(lookup))
        html = f.read()
        pattern = '<div.*?id="content_main".*?>.*?<div.*?class="listing alt".*?>.*?<h3><a[^>]*>(.*?)</a>.*?<span>(.*?)</span>.*?</h3>.*?<p.*?class="listing_address">.*?<span>(.*?)</span>.*?</p>'
        p = re.compile(pattern, re.S);
        m = p.search(html);

        if m and len(m.groups()) == 3:
            name = m.group(1)

            # strip non-numeric characters in phone number
            phone = re.sub('[^0-9]+', '', m.group(2))
            address = m.group(3)
            
            # print. the good old sprintf way
            reply = "Name: %s, Phone: %s, Address: %s" % (name, phone, address)
        else:
            reply = "Sorry! No match :-("

        f.close();

        #reply = ', '.join([ "%s: %s" % (k.encode("UTF-8"), v.encode("UTF-8")) for k, v in data.items() ])
        if reply:
            irc.reply(reply, prefixNick=False)

    tlf = commands.wrap(tlf, [commands.getopts({}), 'text'])

Class = Tlf


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
