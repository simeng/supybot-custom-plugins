###
# Copyright (c) 2011, xt
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

import supyreddit
reload(supyreddit)

class Redditnotify(callbacks.Plugin):
    """Add the help for "@plugin help Redditnotify" here
    This should describe *how* to use this plugin."""

    def __init__(self, irc):
        self.__parent = super(Redditnotify, self)
        self.__parent.__init__(irc)
        self.announced_urls = []

    def reddit(self, irc, msg, args, subreddit):
        try:
            stories = supyreddit.fetch_stories(subreddit, amount=5)
        except Exception, e:
            irc.reply(str(e))
            return
        for story in stories:
            url = story.url
            replies = []
            if not url in self.announced_urls:
                replies.append( '%s: %s %s' %(subreddit, story.title, url))
                self.announced_urls.append(url)
            if replies:
                self._announce(irc, replies)
    reddit = wrap(reddit, ['text'])

    def submit(self, irc, msg, args, title, url):
        supyreddit.submit(title, url)
    submit = wrap(submit, ['text', 'text'])

    def __call__(self, irc, msg):
        self.__parent.__call__(irc, msg)
        irc = callbacks.SimpleProxy(irc, msg)

    def _announce(self, irc, list):
        return irc.replies(list, prefixNick=False)

Class = Redditnotify


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
