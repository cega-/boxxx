#!/usr/bin/python
# -*- coding: utf-8 -*-

import re

filepath = '/tmp/bind_file'
with open(filepath) as fp:  
	line = fp.readline()
	while line:
		domain_name = re.findall('^zone\s\"(.*)\"\sIN\s{', line, re.I)
		if domain_name :
			domain_name = domain_name[0]
			print domain_name
		line = fp.readline()
