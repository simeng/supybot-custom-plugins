###
# -* encoding: UTF-8 *-
# Copyright (c) 2008, Tor Hveem
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

from supybot.commands import *
import supybot.callbacks as callbacks
import supybot.ircmsgs as ircmsgs

class IRCColor(object):
    COLOR_WHITE = 0
    COLOR_BLACK = 1
    COLOR_GREEN = 3
    COLOR_RED = 4
    COLOR_MAGENTA = 6
    COLOR_CYAN = 7
    COLOR_YELLOW = 8
    COLOR_BLUE = 12

    @classmethod
    def colorize(cls, string, color):
        if isinstance(color, basestring):
            color = getattr(cls, 'COLOR_%s' % color.upper())
        #string = "\x03%01d,%01d%s\x03" % (color, cls.COLOR_BLACK, string)
        string = "\x03%01d%s\x03" % (color, string)
        return string

class Meter(callbacks.Plugin):
    """
    Module for Meter stuff
    """

    def meter(self, irc, msg, args, barindex, metertype):
        """
        index type        

        """

        c = IRCColor.colorize
        def white(s):
            #return c(s, 'white')
            return s
        def yellow(s):
            return c(s, 'yellow')
        def red(s):
            return c(s, 'red')
        def green(s):
            return c(s, 'green')
        def black(s):
            return c(s, 'black')
        def magenta(s):
            return c(s, 'magenta')
        def blue(s):
            return c(s, 'blue')


        max = 10
        min = max - (max*2)
        ci = (max*2)/5 # colourint, ci is easier on the eyes
        careneg = '%s' % ("."*max)
        carepos = '%s' % ("."*max)
        carechar = 'X'
	
        try:
            barindex = int(barindex)

            if barindex < 0-max:
                barindex =0-max
            elif barindex > max*2:
                barindex = max*2+1
            
            if barindex > 0:
                carepos = carepos[:barindex-1] + carechar + carepos[barindex:]
                carepos = red(carepos[:4]) + yellow(carepos[4:8]) + green(carepos[8:])
                carestring = '|' + carepos + '|' + " " + metertype + "-o-meter"
            elif barindex < 0:
                barindex = barindex+max
                careneg = careneg[:barindex] + carechar + careneg[barindex+1:]
                careneg = red(careneg[:7]) + yellow(careneg[7:])
                carepos = yellow(carepos[:4]) + green(carepos[4:])
                carestring = '|' + careneg + '|' + carepos + '|' + " " + metertype + "-o-meter"
            else:
                carepos = red(carepos[:4]) + yellow(carepos[4:8]) + green(carepos[8:])
                carestring = '|' + carepos + '|' + " " + metertype + "-o-meter"

            channel = msg.args[0]
            irc.reply(carestring, prefixNick=False)
        except Exception, ex:
            irc.reply(str(ex))
    meter = wrap(meter, ['int', 'text'])
Class = Meter
