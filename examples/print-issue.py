#!/usr/bin/python
# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

#
# This script lists all members of given JIRA group
#

import sys
from pyjira import jira, error

# Enter you jira URL, login and password here:
j = jira.Jira("http://example.com/jira", "alice", "secret")

if len(sys.argv) != 2:
	print "Try: %s issue_key" % sys.argv[0]
	sys.exit(1)

try:
	# get Group object
	i = j.getIssueByKey(sys.argv[1])

	print i.display()
except(error.IssueNotFound):
	print "Issue not found: ‘%s’." % sys.argv[1]
