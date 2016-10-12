#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import re
import sys
import xmlrpclib

import boxxx_main

class BoxxxApp(QtGui.QMainWindow, boxxx_main.Ui_MainWindow):
	def __init__(self):
		# Explaining super is out of the scope of this article
		# So please google it if you're not familar with it
		# Simple reason why we use it here is that it allows us to
		# access variables, methods etc in the boxxx_main.py file
		super(self.__class__, self).__init__()
		self.setupUi(self)  # This is defined in boxxx_main.py file automatically
							# It sets up layout and widgets that are defined
		self.add.clicked.connect(lambda: self.add_zonedns_row(self.input_newdnszone.text()))
		self.t_listdnszone.setColumnCount(2)
		self.t_listdnszone.verticalHeader().setVisible(False)
		self.t_listdnszone.horizontalHeader().setVisible(False)
		self.l_zone_dns = []
		self.l_file_zone_dns = []
		self.url_rpc_server = 'localhost'
		self.port_rpc_server = 9000
		self.bind_file_main_zone_conf = '/tmp/name.option.local'
		self.file_zone_path = '/tmp/db.'
#		self.file_zone_path = '/etc/bind/db.'
		self.rpc_api = xmlrpclib.ServerProxy('http://{0}:{1}/'.format(self.url_rpc_server, self.port_rpc_server))
		self.file_string = self.rpc_api.read_file(self.bind_file_main_zone_conf)
		self.get_zonedns_infile()

	def create_zone_dns(self, dnszone_name):
		template_zone_dns = 'zone "{0}" IN {{\n\t type master;\n\t file "/etc/bind/db.{0}";\n}};\n'.format(dnszone_name)
		return template_zone_dns

	def get_zonedns_infile(self):
		l_line_file = self.file_string.split('\n')
		
		number_of_line = len(l_line_file)
		flag = False

		i = 0
		while i < number_of_line:
			line = l_line_file[i]
			res_regexp = re.search('^zone\s\"(.*)\"\sIN\s{$', line)
			if res_regexp:
				zone_dns = res_regexp.group(1)
				self.l_zone_dns.append(zone_dns)
				if not flag:
					self.l_file_zone_dns.append('<!-- DNS ZONE -->')
					flag = True
				noitem = QtGui.QTableWidgetItem('No action')
				newitem = QtGui.QTableWidgetItem(zone_dns)
				rowPosition = self.t_listdnszone.rowCount()
				self.t_listdnszone.insertRow(rowPosition)
				self.t_listdnszone.setItem(rowPosition, 0, noitem)
				self.t_listdnszone.setItem(rowPosition, 1, newitem)
				while True:
					i += 1
					if i == number_of_line:
						break
					elif re.search('^};$', l_line_file[i]):
						break
			else:
				self.l_file_zone_dns.append(line)
			i += 1

	def send_zone_to_bind(self):
		new_file_zone_ref = ''

		for line in self.l_file_zone_dns:
			if re.search('^<!-- DNS ZONE -->$', line):
				for zone in self.l_zone_dns:
					new_file_zone_ref += self.create_zone_dns(zone)
					self.create_file_zone(zone)
			else:
				new_file_zone_ref += '{0}\n'.format(line)
		self.rpc_api.create_file(self.bind_file_main_zone_conf, new_file_zone_ref)
		self.rpc_api.restart_service(['service', 'resolvconf', 'restart', '>', '/tmp/bind_restart.log'])

	def create_file_zone(self, zone):
		file_entry_dns_zone = ';\n\
; BIND data file for local loopback interface\n\
;\n\
$TTL    604800\n\
@       IN      SOA     ns.{0}. root.localhost. (\n\
                              4         ; Serial\n\
                         604800         ; Refresh\n\
                          86400         ; Retry\n\
                        2419200         ; Expire\n\
                         604800 )       ; Negative Cache TTL\n\
;\n\
@       IN      NS      ns.{0}.\n\
NS      IN      A       192.168.42.1\n\
www     IN      A       192.168.42.1\n\
@       IN      AAAA    ::1\n'.format(zone)

		self.rpc_api.create_file('{0}{1}'.format(self.file_zone_path, zone), file_entry_dns_zone)


	def remove_table_row(self, row_id, dnszone_name):

		self.l_zone_dns.remove(dnszone_name)

		self.rpc_api.remove_file('{0}{1}'.format(self.file_zone_path, dnszone_name))

		row_number = self.t_listdnszone.indexAt(row_id).row()
		self.t_listdnszone.removeRow(row_number)
		self.send_zone_to_bind()

	def add_zonedns_row(self, dnszone_name):
		icon_pxm = QtGui.QPixmap('./poubelle.xpm')
		icon = QtGui.QIcon(icon_pxm)

		rowPosition = self.t_listdnszone.rowCount()

		self.t_listdnszone.insertRow(rowPosition)
		self.l_zone_dns.append(str(dnszone_name))
		newitem = QtGui.QTableWidgetItem(dnszone_name)
		b_action = QtGui.QPushButton('Delete'.format())
		b_action.setIcon(icon)
		b_action.clicked.connect(lambda: self.remove_table_row(b_action.pos(), dnszone_name))

		self.t_listdnszone.setCellWidget(rowPosition, 0, b_action)
		self.t_listdnszone.setItem(rowPosition, 1, newitem)

		self.send_zone_to_bind()

def main():
	app = QtGui.QApplication(sys.argv)  # A new instance of QApplication
	form = BoxxxApp()                 # We set the form to be our BoxxxApp (boxxx_main)
	form.show()                         # Show the form
	app.exec_()                         # and execute the app


if __name__ == '__main__':
	main()