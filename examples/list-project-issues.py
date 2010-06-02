#!/usr/bin/python
# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

#
# This script lists all all open issues in given project
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
	print "Try: %s project_name" % sys.argv[0]
	sys.exit(1)

try:
	print "Issues in %s:" % sys.argv[1]
	for i in r.getProjectByName(sys.argv[1]).getIssues("open"):
		print jira.Issue(j, i).display()
except(jiraError.ProjectNotFound):
	print "Project not found: ‘%s’." % sys.argv[1]
