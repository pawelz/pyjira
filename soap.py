# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

from SOAPpy import WSDL
import jiraError

class Soap(WSDL.Proxy):
	access = {}

	# Public interface

	def __init__(self, URL, username, password):
		"""Authenticates to JIRA (by calling auth method) and reads list of projects."""
		self.access = {"URL": URL, "username": username, "password": password}
		self.auth()

	# Private methods

	def auth(self):
		"""Authenticates to JIRA"""
		WSDL.Proxy.__init__(self, self.wsdllocation())
		self.token = self.login(self.access["username"], self.access["password"])

	def wsdllocation(self):
		"""Returns JIRA SOAP WSDL URL"""
		return self.access["URL"] + '/rpc/soap/jirasoapservice-v2?wsdl'
	
	# Debug/Development methods

	def listSOAPmethods(self):
		"""Prints all available SOAP calls"""
		for key in self.methods.keys():
			print key, ': '
			for param in self.methods[key].inparams:
				print '\t', param.name.ljust(10), param.type
			for param in self.methods[key].outparams:
				print '\tOut: ', param.name.ljust(10), param.type
