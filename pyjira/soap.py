# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

import suds
import error
import config

class Soap(suds.client.Client):
	access = {}

	# Public interface

	def __init__(self, URL=None, username=None, password=None):
		"""Authenticates to JIRA (by calling auth method) and reads list of projects."""
		cfg = config.pyjira()
		self.access = {
			"URL": URL or cfg["url"],
			"username": username or cfg["username"],
			"password": password or cfg["password"]
		}
		self.auth()

	def soap(self, func, *args):
		try:
			return func(self.token, *args)
		except (suds.WebFault):
			self.auth()
			return func(self.token, *args)

	# Private methods

	def auth(self):
		"""Authenticates to JIRA"""
		suds.client.Client.__init__(self, self.wsdllocation())
		self.token = self.service.login(self.access["username"], self.access["password"])

	def wsdllocation(self):
		"""Returns JIRA SOAP WSDL URL"""
		return self.access["URL"] + '/rpc/soap/jirasoapservice-v2?wsdl'
