# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

from SOAPpy import WSDL
import soap
import jiraError

class Jira:
	project = {}
	def __init__(self, j):
		self.soap = j
		for p in self.soap.getProjectsNoSchemes(self.soap.token):
			self.project[p["key"]] = Project(self.soap, p)

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


class Project:
	
	def __init__(self, j, l):
		self.soap                = j
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
	
	def getIssues(self, status="Open"):
		return self.soap.getIssuesFromJqlSearch(self.soap.token, "project = %s and status = %s" % (self.key, status), 300)

	def getNotificationScheme(self):
		return NotificationScheme(self.notificationScheme)

	def getIssueSecurityScheme(self):
		return IssueSecurityScheme(self.issueSecurityScheme)

	def getPermissionScheme(self):
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
