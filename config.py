# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

import os

class config(dict):
	def setFromEnv(self, key, env, default):
		"""Sets configuration key to value of env, or default if env does not exist."""
		try:
			self[key] = os.environ[env]
		except KeyError:
			self[key] = default


class pyjira(config):
	def __init__(self):
		self.setFromEnv("pager",    "PAGER", "more")
		self.setFromEnv("editor",   "EDITOR", "vi")
		self.setFromEnv("url",      "JIRA_URL", "")
		self.setFromEnv("username", "JIRA_USERNAME", "")
		self.setFromEnv("password", "JIRA_PASSWORD", "")
