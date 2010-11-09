###
# Copyright (c) 2010, Michael Peters
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
import supybot.conf as conf
import supybot.registry
import re

class Kohanadocs(callbacks.Plugin):
	"""Add the help for "@plugin help Kohanadocs" here
	This should describe *how* to use this plugin."""
	
	def api(self, irc, msg, args, nick, clas, func):
		"""<class> [<function>] [<nick>]

		Link to API documentation for <class> (<function>), optionally telling it to <nick>"""
		
		# Set the reply to if its set
		if nick != None:
			# Don't allow people to tell to kohana-bot, he gets mad
			if re.match("kohana-bot",nick,flags=re.IGNORECASE):
				irc.reply("He doesn't care.")
				return
			msg.nick = nick
		
		# Build the link
		out = clas
		if type(func) == str:
			match = re.match("\$",func)
			if match is not None:
				out = out + "#property:" + func
			else:
				out = out + "#" + func
		msg = conf.get(conf.supybot.plugins.Kohanadocs.apilink) + out
		
		# And send it
		irc.reply(msg)
	api = wrap(api, [reverse(optional('nickInChannel')), 'somethingWithoutSpaces', optional('somethingWithoutSpaces')])

	def docs(self, irc, msg, args, nick, page):
		"""<page> [<nick>]
		
		Link to the documentation for that <page>, optionally telling it to <nick>. If I don't recognize the page, I will try to guess"""
		
		# Set the reply to if its set
		if nick != None:
			# Don't allow people to tell to kohana-bot, he gets mad
			if re.match("kohana-bot",nick,flags=re.IGNORECASE):
				irc.reply("He doesn't care.")
				return
			msg.nick = nick
		
		# If no page specified, just return a link to the docs
		if page == None:
			msg = conf.get(conf.supybot.plugins.Kohanadocs.doclink)
			irc.reply(msg)
			return
		
		msg = conf.get(conf.supybot.plugins.Kohanadocs.doclink) + page
		irc.reply(msg)
	docs = wrap(docs, [reverse(optional('nickInChannel')), optional('somethingWithoutSpaces')])
	
#	def add(self, irc, msg, args, page, path):
#		"""<page> <path>
#		
#		Adds a link to the documentation with page, <path> must be relative to doclink, and must not have a trailing slash"""
#		pages = conf.supybot.plugins.Kohanadocs.pages
#		pages.register(page,registry.String(path,"""This is a page"""))
#		irc.replySuccess()
#	add = wrap(add, ['somethingWithoutSpaces','somethingWithoutSpaces',("checkCapability", "docs")])


Class = Kohanadocs


# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:
