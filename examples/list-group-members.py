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
	print "Try: %s group_name" % sys.argv[0]
	sys.exit(1)

try:
	# get Group object
	g = j.getGroupByName(sys.argv[1])

	# print its name
	print "Group: %s" % g.raw.name

	# get list of members, and display it
	print '\n\n'.join(map(lambda x: x.display(), g.getMembers())).encode('utf-8')
except(error.GroupNotFound):
	print "Group not found: ‘%s’." % sys.argv[1]
