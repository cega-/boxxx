#!/usr/bin/env python
# -*- coding: utf-8 -*-

import json
import traceback

class ConfClass(object):
	"""docstring for ConfClass"""
	def __init__(self, conf_json_file):
		super(ConfClass, self).__init__()
		self.conf_json_file = conf_json_file
		try:
			print u'-- ConfClass --\n Import configuration from : {0}'.format(self.conf_json_file)
			with open(self.conf_json_file) as fd_json_file:
				self.conf = json.load(fd_json_file)
		except Exception, e:
			print u'-- ConfClass --\n Issue into init: {0}\n Error stack : {1}\n'.format(e, traceback.format_exc())
			raise e