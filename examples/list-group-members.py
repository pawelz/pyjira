#!/usr/bin/python
# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

#
# This script lists all members of given JIRA group
#

import sys
import soap
import jira
import jiraError
import config

cfg = config.pyjira()
j = soap.Soap(cfg["url"], cfg["username"], cfg["password"])

r = jira.Jira(j)

if len(sys.argv) != 2:
	print "Try: %s group_name" % sys.argv[0]
	sys.exit(1)

try:
	# get Group object
	g = r.getGroupByName(sys.argv[1])

	# print its name
	print "Group: %s" % g.name

	# get list of members, and display it
	print '\n\n'.join(map(lambda x: x.display(), g.getMembers())).encode('utf-8')
except(jiraError.GroupNotFound):
	print "Group not found: ‘%s’." % sys.argv[1]
