
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
lookup unicode codepoints
'''

import supybot.utils as utils
#from supybot.commands import *
from supybot import commands
import supybot.plugins as plugins
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs

#sys.path.insert('/home/alexis/plugins/WTF8')
import sys
import unicodedata

import codepoints
reload(codepoints)

class WTF8(callbacks.Plugin):
    """Add the help for "@plugin help WTF8" here
    This should describe *how* to use this plugin."""

    def u(self, irc, msg, args, opts, lookup):
        '''
        <codepoint lookup string>
        '''
        replies = codepoints.codepoint_simple(lookup)

        reply = ','.join(replies)
        if reply:
            irc.reply(reply.lower(), prefixNick=False)

    u = commands.wrap(u, [commands.getopts({}), 'text'])

    def w(self, irc, msg, args, opts, lookup):
        '''
        <reverse codepoint lookup string>
        '''

        try:
            lookup = lookup.decode('utf-8')
        except:
            pass
        if not isinstance(lookup, unicode):
            try:
                lookup = lookup.decode('iso-8859-1')
            except:
                pass
        assert isinstance(lookup, unicode)

        replies = []
        for uchar in lookup:
            try:
                name = unicodedata.name(uchar)
            except ValueError:
                continue
            cp = ord(uchar)
            replies.append(codepoints.about(uchar, cp, name))

        reply = ','.join(replies)
        if reply:
            irc.reply(reply.lower(), prefixNick=False)

    w = commands.wrap(w, [commands.getopts({}), 'text'])

Class = WTF8


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
