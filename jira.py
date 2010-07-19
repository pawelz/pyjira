# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

from suds import WebFault as SOAPError
import sys
import soap
import types
import datetime

import jiraError

class JiraObject:
	"""
	‘Virtual’ class for all Jira objects like Project, Issue, User,
	NotificationScheme etc.
	"""

	_specialFields = ['id', 'raw']

	sudsType = ""

	def __init__(self, s, l):
		self.jira = s

		# [pl] Jeżeli l jest Null, tworzymy pusty obiekt danego typu
		if (type(l) == types.NoneType):
			self.raw = s.factory.create(self.sudsType)
			self.default()
		# [pl] w przeciwnym przypadku l jest obiektem suds.
		else:
			self.raw = l

		### Useful for debug purposes
		### print self.raw

	def fields(self):
		"""Returns list of all JIRA fields"""
		# filter out all _special fields
		return filter(lambda x: str(x)[0] != '_', self.raw.__dict__)

	def maxlen(self):
		"""Compute maximal field name, and cache result in self._max variable"""
		# This is a bit tricky. It sets _max iff it is not set yet.
		return self.__dict__.setdefault('_max', reduce(max, map(len, self.fields())))

	def display(self):
		"""
		Returns pretty-printed object information, excluding _specialFields

		Classes that inherit JiraObject are supposed to overload this
		function, to handle _specialFields.
		"""
		# generate iterator that iterates through all non special fields
		fields = (str(x).decode("UTF-8") for x in self.fields() if x not in self._specialFields)

		# return table containing all these fields
		return '\n'.join([" %s%s : %s" % (' '*(self.maxlen()-len(f)), f, self.raw.__dict__[f]) for f in fields])

	def default(self):
		"""
		This method is being executed when *NEW* object is created. By default
		it does nothing. Overload it to initialize some default values of jira
		fields, like:

		self.raw.author=self.jira.access["username"]
		self.raw.created = datetime.datetime.now()
		"""
		pass

	def __str__(self):
		"""
		Returns main JIRA object identifier.

		It's quite tricky, yet very handy. Many JIRA API calls operate on
		keys, or names. So if we pass str(user) we don't have to care whether
		user is users name, or it is User object.
		"""
		try:
			return self.raw.key
		except AttributeError:
			try:
				return self.raw.name
			except AttributeError as e:
				raise jiraError.CantCastToString(e)

class Jira(soap.Soap):
	"""
	Class representing Jira instance. Note that this class does not inherits
	JiraObject class.
	"""
	project = []
	def __init__(self, url, username, password):
		soap.Soap.__init__(self, url, username, password)
		project = [x.name for x in self.service.getProjectsNoSchemes(self.token)]

	def getProject(self, k):
		"""
		If k is string, interpret it as project KEY. Otherwise just return k.
		This way we can type getProject(p) and we don't have to care wether k
		is Project or KEY.

		TODO: cache projects fetched from JIRA.
		"""
		print type(k), str(k)
		if type(k) == types.StringType or type(k) == types.UnicodeType:
			return Project(self, self.service.getProjectByKey(self.token, k))
		return k

	# def getProjectById(self, i):
	# 	"""Returns project with given Id."""
	# 	return self.project[k]
	# 	for p in self.project:
	# 		if self.project[p].id == i:
	# 			return self.project[p]
	# 	raise jiraError.ProjectNotFound(p)

	# def getProjectByName(self, n):
	# 	"""Returns project with given name."""
	# 	for p in self.project:
	# 		if self.project[p].name == n:
	# 			return self.project[p]
	# 	raise jiraError.ProjectNotFound()

	def getGroupByName(self, n):
		"""Returns group with given name."""
		try:
			return Group(self, self.service.getGroup(self.token, n))
		except SOAPError as e:
			raise jiraError.GroupNotFound(e)
	
	def getUserByName(self, n):
		"""Returns user with given name."""
		try:
			return User(self, self.service.getUser(self.token, n))
		except SOAPError as e:
			raise jiraError.UserNotFound(e)
	
	def getIssueByKey(self, k):
		"""Returns issue with given key."""
		try:
			return Issue(self, self.service.getIssue(self.token, k))
		except SOAPError as e:
			raise jiraError.IssueNotFound(e)

class Project(JiraObject):
	issueTypes = []

	def __init__(self, j, r):
		JiraObject.__init__(self, j, r)
		self.issueTypes = self.jira.service.getIssueTypesForProject(self.jira.token, self.raw.id)

	def issueTypeIdByName(self, n):
		"""
		Returns id of issueType with given name.

		If issueType is not valid for given project, raises InvalidIssueType
		exception.
		"""
		try:
			return [x.id for x in self.issueTypes if x.name == n][0]
		except IndexError:
			raise InvalidIssueType(n)

	def issueTypeNameById(self, i):
		"""
		Returns name of issueType with given id.

		If issueType is not valid for given project, raises InvalidIssueType
		exception.
		"""
		try:
			return [x.name for x in self.issueTypes if x.id == i][0]
		except IndexError:
			raise InvalidIssueType(i)

	def getIssues(self, status="Open"):
		return [Issue(self.jira, x, self) for x in self.jira.service.getIssuesFromJqlSearch(self.jira.token, "project = %s and status = %s" % (self.raw.key, status), 300)]

	def getLead(self):
		return self.jira.service.getUser(self.jira.token, self.raw.lead)

	def getNotificationScheme(self):
		return NotificationScheme(self.raw.notificationScheme)

	def getIssueSecurityScheme(self):
		return IssueSecurityScheme(self.raw.issueSecurityScheme)

	def getPermissionScheme(self):
		return PermissionScheme(self.raw.permissionScheme)

class Issue(JiraObject):
	_specialFields = ['id', 'raw', 'key', 'type', 'summary', 'description', 'reporter', 'assignee']
	_comments = []
	project=None
	sudsType = "tns1:RemoteIssue"

	def __init__(self, j, r=None, p=None):
		JiraObject.__init__(self, j, r)
		if r:
			self._comments=self.jira.service.getComments(self.jira.token, self.raw.key)

		# [pl] Logika:
		#      Jeżeli dostaliśmy p (jako Project lub String) ustawiamy project
		#      na to co dostaliśmy.
		#      Jeżeli nie dostaliśmy p ale mamy key, ustawiamy project na
		#      podstawie key.
		#      Ostatecznie fallback na None

		if p:
			self.project=self.jira.getProject(p)
		else:
			try:
				self.project=self.jira.getProject(self.raw.key[0:self.raw.key.find('-')])
			except TypeError: # TypeError: 'NoneType' object is unsubscriptable
				pass

	def default(self):
		self.raw.reporter=self.jira.access["username"]
		self.raw.created = datetime.datetime.now()
		self.raw.updated = datetime.datetime.now()

	def display(self):
		return '[%s] (%s => %s) %s: %s\n%s\n\n%s\n%s\n' % (
				self.raw.key,
				self.raw.reporter,
				self.raw.assignee,
				self.project and self.project.issueTypeNameById(self.raw.type) or "None",
				self.raw.summary,
				JiraObject.display(self),
				self.raw.description,
				'\n\n'.join([str(i).decode("UTF-8") for i in self._comments]))
	
	def comment(self, c):
		"""
		Adds comment to the issue.
		Accepts Comment object, or just string as an argument.
		"""
		if (type(c) == types.StringType):
			cmnt = Comment(self.jira)
			cmnt.raw.body = c
		else:
			cmnt = c

		self.jira.service.addComment(self.jira.token, self.raw.key, cmnt.raw)
		self._comments=self.jira.service.getComments(self.jira.token, self.raw.key)
	
class NotificationScheme(JiraObject):
	sudsType = "TODO:unknown"
	pass

class IssueSecurityScheme(JiraObject):
	sudsType = "TODO:unknown"
	pass

class IssueType(JiraObject):
	sudsType = "TODO:unknown"
	pass

class PermissionScheme(JiraObject):
	sudsType = "TODO:unknown"
	pass

class User(JiraObject):
	sudsType = "TODO:unknown"
	pass

class Group(JiraObject):
	sudsType = "TODO:unknown"
	def getMembers(self):
		# Yeaahhh, functional overdoze
		return [User(self.jira, x) for x in self.raw.users if x]

	def removeUser(self, u):
		try:
			self.jira.service.removeUserFromGroup(self.jira.token, self.raw, u.raw)
		except SOAPError as e:
			raise jiraError.OperationFailed(e)

class Comment(JiraObject):
	sudsType = "tns1:RemoteComment"
	def __init__(self, j):
		JiraObject.__init__(self, j, None)

	def default(self):
		self.raw.author = self.jira.access["username"]
		self.raw.updateAuthor = self.jira.access["username"]
		self.raw.created = datetime.datetime.now()
		self.raw.updated = datetime.datetime.now()
