#!/usr/bin/python
# -*- coding: utf-8 -*-

import re
import socket

from subprocess import Popen, PIPE, call, check_call

filepath = '/tmp'
filename = 'dhcp.lease'
ipod_mac = 'a4:2b:b0:e1:3c:f6'
ip_lease_to_ipod = None
tmp_ip = ''

with open('{0}/{1}'.format(filepath, filename)) as fp:  
	line = fp.readline()
	while line:
		ip_lease = re.findall('^\s*lease\s+((25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?))\s*[{\n]', line, re.I)
		if ip_lease :
			tmp_ip = ip_lease[0][0]
		hardware_mac = re.findall('^\s*hardware\s+ethernet\s+(([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2}))\s*;', line, re.I)
		if hardware_mac :
			if hardware_mac[0][0] == ipod_mac:
				ip_lease_to_ipod = tmp_ip

		line = fp.readline()

if ip_lease_to_ipod:
	try:
		socket.gethostbyaddr(ip_lease_to_ipod)
		print ip_lease_to_ipod
	except socket.herror:
		print u'Unknown host'
		raise e

	try:
		sp_ipod = Popen(['sshpass -p "alpine" scp -i /root/.ssh/im_cluster_sync_key root@{0}:clients_im* /etc/freeradius/'.format(ip_lease_to_ipod)], shell=True, stdout=PIPE, stderr=PIPE)
		stdout, stderrno = sp_ipod.communicate()
		if stdout != '' or stderrno != '':
			print 'SCP Radius STDOUT: {0}\nSTDERRNO: {1}'.format(stdout, stderrno)
	except Exception, e:
		raise e