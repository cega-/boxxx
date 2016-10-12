#!/usr/bin/python
# -*- coding: utf-8 -*-

import os

from SimpleXMLRPCServer import SimpleXMLRPCServer
from subprocess import Popen

def create_file(filename_inc_path, content):
	fd = open(filename_inc_path, 'w')
	fd.write(content)
	fd.close()

def read_file(filename_inc_path):
	fd = open(filename_inc_path, 'r')
	content = fd.read()
	fd.close()
	return content

def remove_file(filename_inc_path):
	os.remove(filename_inc_path)

def restart_service(l_args):
	Popen(l_args)

server_rpc = SimpleXMLRPCServer(('0.0.0.0', 9000), logRequests=True, allow_none=True)
server_rpc.register_function(create_file)
server_rpc.register_function(read_file)
server_rpc.register_function(remove_file)
server_rpc.register_function(restart_service)

server_rpc.serve_forever()