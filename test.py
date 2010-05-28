#!/usr/bin/python
# vim:fileencoding=utf-8

# Copyright: © 2009, 2010 TouK sp. z o.o. s.k.a.
# Author:    Paweł Zuzelski <pzz@touk.pl>

import sys
import jira
import jiraError
import config

cfg = config.pyjira()
j = jira.Jira(cfg["url"], cfg["username"], cfg["password"])

if len(sys.argv) != 2:
	print "Try: %s project_name" % sys.argv[0]
	sys.exit(1)

try:
	print "The leader of ‘%s’ project is ‘%s’." % (sys.argv[1], j.getProjectByName(sys.argv[1]).lead)
except(jiraError.ProjectNotFound):
	print "Project not found: ‘%s’." % sys.argv[1]
