# vim:fileencoding=utf-8

# Copyright: © 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

import os
import sys

class JiraError(Exception):
	importance = 9

	def __init__(self, e):
		Exception.__init__(self, e)
		try:
			if int(os.environ["PYJIRA_DEBUG"]) > self.importance:
				print >>sys.stderr, "[PYJIRA]: %s" % str(self)
		except KeyError:
			pass
	
class NotImplementedYet(JiraError):
	importance = 1

class CantCastToString(JiraError):
	importance = 1

class ProjectNotFound(JiraError):
	importance = 1

	def __str__(self):
		return "Project %s not found" % JiraError.__str__(self)

class GroupNotFound(JiraError):
	importance = 1

	def __str__(self):
		return "Group %s not found" % JiraError.__str__(self)

class UserNotFound(JiraError):
	importance = 1

class IssueNotFound(JiraError):
	importance = 1

class OperationFailed(JiraError):
	importance = 1

class InvalidIssueType(JiraError):
	importance = 1

	def __str__(self):
		return "Invalid issueType: %s" % JiraError.__str__(self)
