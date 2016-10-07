#!/usr/bin/python
# -*- coding: utf-8 -*-

from PyQt4 import QtGui
import re
import sys

import boxxx_main

###regexp "^zone\s\"(.*)\"\sIN\s{$"

file_string = 'Coucou\n\
zone "vk.com" IN {\n\
        type master;\n\
        file "/etc/bind/db.vk.com";\n\
};\n\
zone "cega.lan" IN {\n\
        type master;\n\
        file "/etc/bind/db.cega.lan";\n\
};\n\
zone "test.lan" IN {\n\
        type master;\n\
        file "/etc/bind/db.test.lan";\n\
};\n\
\##Supervouvou'

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
		self.get_zonedns_infile()

	def create_zone_dns(self, dnszone_name):
		template_zone_dns = 'zone "{0}" IN {{\n\t type master;\n\t file "/etc/bind/db.{0}";\n}};\n'.format(dnszone_name)
		return template_zone_dns

	def get_zonedns_infile(self):
		l_line_file = file_string.split('\n')
		
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

		print self.l_file_zone_dns

	def send_zone_to_bind(self):
		new_file_zone_ref = ''

		for line in self.l_file_zone_dns:
			if re.search('^<!-- DNS ZONE -->$', line):
				for zone in self.l_zone_dns:
					new_file_zone_ref += self.create_zone_dns(zone)
			else:
				new_file_zone_ref += '{0}\n'.format(line)
#		send_rpc
		print new_file_zone_ref

#	def creation du fichier de reference pour la zone(self):
#		pass

	def remove_table_row(self, row_id, dnszone_name):

		self.l_zone_dns.remove(dnszone_name)

		row_number = self.t_listdnszone.indexAt(row_id).row()
		self.t_listdnszone.removeRow(row_number)

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