###
# Copyright (c) 2009, Simen Graaten
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

import supybot.utils as utils
from supybot.commands import *
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs
import re
import urllib2

class Spotify(callbacks.Plugin):
    """Add the help for "@plugin help Spotify" here
    This should describe *how* to use this plugin."""

    def doPrivmsg(self, irc, msg):
        channel = msg.args[0]

        if irc.isChannel(channel):
            if ircmsgs.isAction(msg):
                message = ircmsgs.unAction(msg)
            else:
                message = msg.args[1]

            m = re.search("(http://open.spotify.com/|spotify:)(?P<type>album|artist|track)([:/])(?P<spoturi>[a-zA-Z0-9]+)/?", message)
            if m:
                r = m.groupdict()
                reply = self.fetch(r['type'], r['spoturi'])
                if reply:
                    irc.queueMsg(ircmsgs.privmsg(channel, reply))

    def fetch(self, type, uri):
        req = urllib2.Request("http://spotify.url.fi/%s/%s?txt" % (type, uri))
        opener = urllib2.build_opener()
        req.add_header("User-agent", "irssi/0.8.12 Python-urllib/2.1")
        data = opener.open(req).read()
        return data

Class = Spotify


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
