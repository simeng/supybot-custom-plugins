###
# -*- coding: UTF-8 -*-
# Copyright (c) 2009, Tor Hveem
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
import supybot.ircmsgs as ircmsgs
import supybot.ircutils as ircutils
import supybot.callbacks as callbacks

class Sylfest(callbacks.Plugin):
    """
    Plugin to kick user in event of broken language
    """

    def _checkWord(self, word):
        self.log.debug("Checking word: %s" %word)

        word = word.rstrip('?') ## har du skrudd av TV'en?
        word = word.rstrip('.')
        word = word.rstrip(',')
        word = word.rstrip('!')
        word = word.replace('`', "'")
        word = word.replace('´', "'")
        
        badends = ("'en", "'a", "'et", "'ern")
        badendsexceptions = ["farad'n", "guns'n"]
        badendsexceptions.extend(self.registryValue('badendsexceptions'))
        
        for badend in badends:
            if word.lower().endswith(badend):
                if word == badend:
                    continue
                if not word.lower() in badendsexceptions:
                    return True


    def doPrivmsg(self, irc, msg):
        channel = msg.args[0]
        if channel in self.registryValue('targets'):
            if irc.isChannel(channel):
                if ircmsgs.isAction(msg):
                    text = ircmsgs.unAction(msg)
                else:
                    text = msg.args[1]

                startswithexceptions = ('"', "'", "-", " -")
                for startswithexception in startswithexceptions:
                    if text.startswith(startswithexception):
                        # Wuhu ! Exception !
                        return

                for word in text.split(' '):
                    if self._checkWord(word):
                        irc.queueMsg(ircmsgs.kick(channel, msg.nick, 'Sylfest likar ikkje %s' %word))
                        #irc.queueMsg(ircmsgs.privmsg(channel, 'Sylfest likar ikkje %s' %word))
                        # break. no need to check further
                        break

Class = Sylfest


# vim:set shiftwidth=4 tabstop=4 expandtab textwidth=79:
