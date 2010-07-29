#!/usr/bin/python
# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

#
# This script lists all all open issues in given project
#

import sys
from pyjira import jira, error

# Enter you jira URL, login and password here:
j = jira.Jira("http://example.com/jira", "alice", "secret")

if len(sys.argv) != 2:
	print "Try: %s project_name" % sys.argv[0]
	sys.exit(1)

try:
	print "Issues in %s:" % sys.argv[1]
	project = j.getProject(sys.argv[1])
	for i in project.getIssues("open"):
		print "%s: %s" % (i.raw.key, i.raw.summary)
		# You can also display full information about each issue instead:
		# print i.display()
except(error.ProjectNotFound):
	print "Project not found: ‘%s’." % sys.argv[1]
