# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

from SOAPpy import WSDL
import jiraError

class Jira(WSDL.Proxy):
	access = {}
	project = {}

	# Public interface

	def __init__(self, URL, username, password):
		"""Authenticates to JIRA (by calling auth method) and reads list of projects."""
		self.access = {"URL": URL, "username": username, "password": password}
		self.auth()
		for p in self.getProjectsNoSchemes(self.token):
			self.project[p["key"]] = Project(p)

	def getProject(self, k):
		"""Returns project with given KEY."""
		return project["k"]

	def getProjectById(self, i):
		"""Returns project with given Id."""
		return project["k"]
		for p in self.project:
			if self.project[p].id == i:
				return self.project[p]
		raise jiraError.ProjectNotFound()

	def getProjectByName(self, n):
		"""Returns project with given Name."""
		for p in self.project:
			if self.project[p].name == n:
				return self.project[p]
		raise jiraError.ProjectNotFound()

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

class Project:
	def __init__(self, l):
		self.projectUrl          = l["projectUrl"]
		self.name                = l["name"]
		self.lead                = l["lead"]
		self.url                 = l["url"]
		self.key                 = l["key"]
		self.description         = l["description"]
		self.notificationScheme  = l["notificationScheme"]
		self.issueSecurityScheme = l["issueSecurityScheme"]
		self.permissionScheme    = l["permissionScheme"]
		self.id                  = int(l["id"])
	
	def getNotificationScheme():
		return NotificationScheme(self.notificationScheme)

	def getIssueSecurityScheme():
		return IssueSecurityScheme(self.issueSecurityScheme)

	def getPermissionScheme():
		return PermissionScheme(self.permissionScheme)

class NotificationScheme():
	def __init__(self, s):
		raise jiraError.NotImplementedYet()

class IssueSecurityScheme():
	def __init__(self, s):
		raise jiraError.NotImplementedYet()

class PermissionScheme():
	def __init__(self, s):
		raise jiraError.NotImplementedYet()
