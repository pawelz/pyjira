# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

from SOAPpy import WSDL
from SOAPpy.Types import faultType as SOAPError
import soap
import jiraError

class JiraObject:
	"""
	‘Virtual’ class for all Jira objects like Project, Issue, User,
	NotificationScheme etc.
	"""

	_specialFields = ['id']

	def __init__(self, s, l):
		"""
		Creates JiraObject fields based on dictionary object as returned by
		Jira SOAP API.
		"""
		self._soap = s
		self.raw = l
		map(lambda x: self.__dict__.update([(x, l[x])]), l._asdict())
	
	def fields(self):
		"""
		Returns list of all JIRA fields

		Actually it returns all class fields that are not methodes and whose
		names does not begin with '_'.
		"""
		return filter(lambda x: type(self.__dict__[x]) != type(self.fields) and x[0] != '_', self.__dict__)

	def maxlen(self):
		"""Compute maximal field name, and cache result in self._max variable"""
		return self.__dict__.setdefault('_max', reduce(max, map(len, self.fields())))

	def display(self):
		"""
		Returns pretty-printed object information, excluding _specialFields

		Classes that inherit JiraObject are supposed to overload this
		function, to handle _specialFields.
		"""
		fields = filter(lambda x: x not in self._specialFields, self.fields())
		return '\n'.join(map(lambda f: " %s%s : %s" % (' '*(self.maxlen()-len(f)), f, self.__dict__[f]), fields))

	def __str__(self):
		"""
		Returns main JIRA object identifier.

		It's quite tricky, yet very handy. Many JIRA API calls operate on
		keys, or names. So if we pass str(user) we don't have to care whether
		user is users name, or it is User object.
		"""
		try:
			return self.key
		except (AttributeError):
			return self.name
		except (AttributeError):
			raise jiraError.CantCastToString()

class Jira:
	"""
	Class representing Jira instance. Note that this class does not inherits
	JiraObject class.
	"""
	project = {}
	def __init__(self, j):
		self._soap = j
		for p in self._soap.getProjectsNoSchemes(self._soap.token):
			self.project[p["key"]] = Project(self._soap, p)

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
		"""Returns project with given name."""
		for p in self.project:
			if self.project[p].name == n:
				return self.project[p]
		raise jiraError.ProjectNotFound()

	def getGroupByName(self, n):
		"""Returns group with given name."""
		try:
			return Group(self._soap, self._soap.getGroup(self._soap.token, n))
		except(SOAPError):
			raise jiraError.GroupNotFound
	
	def getUserByName(self, n):
		"""Returns user with given name."""
		try:
			return User(self._soap, self._soap.getUser(self._soap.token, n))
		except(SOAPError):
			raise jiraError.UserNotFound
	
class Project(JiraObject):
	def getIssues(self, status="Open"):
		return self._soap.getIssuesFromJqlSearch(self._soap.token, "project = %s and status = %s" % (self.key, status), 300)

	def getLead(self):
		return self._soap.getUser(self._soap.token, self.lead)

	def getNotificationScheme(self):
		return NotificationScheme(self.notificationScheme)

	def getIssueSecurityScheme(self):
		return IssueSecurityScheme(self.issueSecurityScheme)

	def getPermissionScheme(self):
		return PermissionScheme(self.permissionScheme)

class Issue(JiraObject):
	_specialFields = ['key', 'summary', 'description', 'reporter', 'assignee']

	def display(self):
		return '[%s] (%s => %s) %s\n%s\n%s\n\n' % (
				self.key,
				self.reporter,
				self.summary,
				self.assignee,
				JiraObject.display(self),
				self.description)

class NotificationScheme(JiraObject):
	pass

class IssueSecurityScheme(JiraObject):
	pass

class PermissionScheme(JiraObject):
	pass

class User(JiraObject):
	pass

class Group(JiraObject):
	def getMembers(self):
		# Yeaahhh, functional overdoze
		return map(lambda x: User(self._soap, x), filter(lambda x: x, self.users))

	def removeUser(self, u):
		self._soap.removeUserFromGroup(self._soap.token, self.raw, u.raw)
