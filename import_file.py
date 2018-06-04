#!/usr/bin/python
# -*- coding: utf-8 -*-

import argparse
import mysql.connector
import sys

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

filepath = ''
file_type_bind = False

def create_dns_entry(domain_name, cur, cnx):
## Add domain
	domain_data = {'domain_name': domain_name, 'type': 'NATIVE'}
	cur.execute(add_domain, domain_data)
	domain_id = cur.lastrowid

## Declare SOA
	soa_entry = 'ns.{0} empty.empty 1 3600 600 604800 3600'.format(domain_name)
	records_data = {'domain_id': domain_id, 'domain_name': domain_name, 'records_content': soa_entry, 'records_type': 'SOA'}
	cur.execute(add_records, records_data)

## Declare NS
	ns_entry = 'ns.{0}'.format(domain_name)
	records_data = {'domain_id': domain_id, 'domain_name': domain_name, 'records_content': ns_entry, 'records_type': 'NS'}
	cur.execute(add_records, records_data)

## Declare A for NS
	a_entry = ip_boxxx
	records_data = {'domain_id': domain_id, 'domain_name': 'ns.{0}'.format(domain_name), 'records_content': a_entry, 'records_type': 'A'}
	cur.execute(add_records, records_data)

## Declare A for domain
	a_entry = ip_boxxx
	records_data = {'domain_id': domain_id, 'domain_name': '{0}'.format(domain_name), 'records_content': a_entry, 'records_type': 'A'}
	cur.execute(add_records, records_data)

## Declare A for *.domain
	a_entry = ip_boxxx
	records_data = {'domain_id': domain_id, 'domain_name': '*.{0}'.format(domain_name), 'records_content': a_entry, 'records_type': 'A'}
	cur.execute(add_records, records_data)

	cnx.commit()

def main(argv):

	parser = argparse.ArgumentParser()
	parser.add_argument('-b', '--bind_file', help='File format to import is BIND', action='store_true')
	parser.add_argument('file_to_import', help='Path to file to import')
	args = parser.parse_args()

	global filepath
	filepath = args.file_to_import

	if args.bind_file:
		global file_type_bind
		file_type_bind = True

if __name__ == "__main__":
	main(sys.argv[1:])

config = {
	'user': 'pdns',
	'password': 'pdns-tgbyhn89?M',
	'host': '127.0.0.1',
	'database': 'pdns'
}

cnx = cur = None
try:
	cnx = mysql.connector.connect(**config)

	ip_boxxx = '188.108.5.119'

	add_domain_tmp = ('INSERT INTO domains_tmp '
					'(name, type) '
					'VALUES (%(domain_name)s, %(type)s)')

	add_domain = ('INSERT INTO domains '
					'(name, type) '
					'VALUES (%(domain_name)s, %(type)s)')

	add_records = ('INSERT INTO records '
						'(domain_id, name, content, type, ttl, prio) '
						'VALUES (%(domain_id)s,%(domain_name)s,%(records_content)s,%(records_type)s,86400,NULL)')

except mysql.connector.Error as err:
	if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
		print('Something is wrong with your user name or password')
	elif err.errno == errorcode.ER_BAD_DB_ERROR:
		print("Database does not exist")
	else:
		print(err)
else:
	cur = cnx.cursor()

	cur.execute('TRUNCATE TABLE domains_tmp')
	cnx.commit()

	with open(filepath) as fp:  
		line = fp.readline()
		while line:

			if file_type_bind == True:
				domain_name = re.findall('^zone\s\"(.*)\"\sIN\s{', line, re.I)
				if domain_name :
					domain_name = domain_name[0]
			else:
				domain_name = line.strip()
			
			if domain_name:
				domain_data = {'domain_name': domain_name, 'type': 'NATIVE'}
				cur.execute(add_domain_tmp, domain_data)

			line = fp.readline()

		cnx.commit()

	cur.execute(
		'SELECT dt.name from domains_tmp dt LEFT JOIN domains d ON dt.name = d.name WHERE d.name IS NULL'
	)

	for row in cur.fetchall():
		if row[0]:
			create_dns_entry(row[0], cur, cnx)

	cur.execute('show databases;')
	for row in cur.fetchall():
		print(row)

finally:
	if cur:
		cur.close()
	if cnx:
		cnx.close()

'''
## Add domain
	domain_data = {'domain_name': domain_name, 'type': 'NATIVE'}
	cur.execute(add_domain, domain_data)
	domain_id = cur.lastrowid

## Declare SOA
	soa_entry = 'ns.{0} empty.empty 1 3600 600 604800 3600'.format(domain_name)
	records_data = {'domain_id': domain_id, 'domain_name': domain_name, 'records_content': soa_entry, 'records_type': 'SOA'}
	cur.execute(add_records, records_data)

## Declare NS
	ns_entry = 'ns.{0}'.format(domain_name)
	records_data = {'domain_id': domain_id, 'domain_name': domain_name, 'records_content': ns_entry, 'records_type': 'NS'}
	cur.execute(add_records, records_data)

## Declare A for NS
	a_entry = ip_boxxx
	records_data = {'domain_id': domain_id, 'domain_name': 'ns.{0}'.format(domain_name), 'records_content': a_entry, 'records_type': 'A'}
	cur.execute(add_records, records_data)

## Declare A for domain
	a_entry = ip_boxxx
	records_data = {'domain_id': domain_id, 'domain_name': '{0}'.format(domain_name), 'records_content': a_entry, 'records_type': 'A'}
	cur.execute(add_records, records_data)

## Declare A for *.domain
	a_entry = ip_boxxx
	records_data = {'domain_id': domain_id, 'domain_name': '*.{0}'.format(domain_name), 'records_content': a_entry, 'records_type': 'A'}
	cur.execute(add_records, records_data)

	cnx.commit()
'''