#!/usr/bin/python
# -*- coding: utf-8 -*-

import mysql.connector
from mysql.connector import errorcode

'''
filepath = '/tmp/adult/domains'
with open(filepath) as fp:  
	line = fp.readline()
	cnt = 1
	while line:
		print("Line {}: {}".format(cnt, line.strip()))
		line = fp.readline()
		cnt += 1
'''

config = {
	'user': 'pdns',
	'password': 'pdns-tgbyhn89?M',
	'host': '127.0.0.1',
	'database': 'pdns'
}

cnx = cur = None
try:
	cnx = mysql.connector.connect(**config)

	add_domain = ('INSERT INTO domains_tmp '
					'(name, type) '
					'values (%(domain_name)s, %(type)s)')

except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print('Something is wrong with your user name or password')
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cur = cnx.cursor()

	filepath = '/tmp/adult/domains'
	with open(filepath) as fp:  
		line = fp.readline()
		cnt = 1
		while line:
##			print("Line {}: {}".format(cnt, line.strip()))
			domain_data = {'domain_name': line.strip(), 'type': 'NATIVE'}
			cur.execute(add_domain, domain_data)
			line = fp.readline()
			cnt += 1

	cnx.commit()
	cur.execute('show databases;')
	for row in cur.fetchall():
		print(row)
finally:
	if cur:
		cur.close()
	if cnx:
		cnx.close()