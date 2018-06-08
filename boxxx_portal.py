#!/usr/bin/python
# -*- coding: utf-8 -*-

import bottle as boxxx
import boxxx_conf_class
import gettext
import logging
import os.path
import setproctitle
import traceback

from beaker.middleware import SessionMiddleware
from bottle import Bottle, route, run, template, request, response, static_file, redirect
from jinja2 import Environment, FileSystemLoader, Template
from os import listdir
from os.path import isfile, join

dir_path = os.path.dirname(os.path.realpath(__file__))
iconf = boxxx_conf_class.ConfClass('{0}/boxxx_portal.conf'.format(dir_path))
Conf = iconf.conf

session_opts = {
	'session.type': 'file',
	'session.cookie_expires': True,
	'session.timeout': 28800,
	'session.data_dir': '{0}/web_session'.format(dir_path),
	'session.auto': True
}


if not os.path.isfile(Conf['log']['file']):
	path, filename = os.path.split(Conf['log']['file'])
	if not os.path.isdir(path) :
		os.makedirs(path)
	open(Conf['log']['file'], 'a').close()


# create logger
logger = logging.getLogger('boxxx')
logger.setLevel(eval(Conf['log']['debug_level']))

# create console handler and set level to debug
ch = logging.FileHandler(Conf['log']['file'])
ch.setLevel(eval(Conf['log']['debug_level']))

# create formatter
formatter = logging.Formatter(fmt='%(asctime)s :: %(levelname)s :: %(message)s', datefmt='%m/%d/%Y %H:%M:%S')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)


try:
	logger.info('Initialize Boxxx portal env'.format())
	setproctitle.setproctitle('Boxxx')
###	IMDB_psg = DBManagement_postgres()
	app = boxxx.default_app()
	app = SessionMiddleware(app, session_opts)

#	t = gettext.translation('boxxx', 'translation', ['fr'], fallback=False)
#	_ = t.ugettext
	env = Environment(loader=FileSystemLoader('{0}/templates'.format(dir_path)), extensions=['jinja2.ext.i18n'])
#	env.install_gettext_translations(t)
	l_templates = env.list_templates(extensions=['tpl'])
	
except Exception, e:
	logger.error(u'-- Init Boxxx Portal --\n Issue into env init: {0}\n Error stack : {1}\n'.format(e, traceback.format_exc()))
	raise e

def jsonp(request, dictionary):
	if (request.query.callback):
		return "%s(%s)" % (request.query.callback, json.dumps(dictionary))
	return json.dumps(dictionary)

@boxxx.route('/web/<filepath:path>')
def server_static(filepath):
	return static_file(filepath, root='web/')

@boxxx.post('/im_get_doc_freeradius')
@boxxx.get('/im_get_doc_freeradius')
def A_getDoc_freeradius():
	response.content_type = 'application/json'
	val_ret = {"more": False, "results":[], 'doc': {}}
	oldID = None

	uid = request.query.get('uid')
	collection = request.query.get('collection')
	fields = request.query.get('fields')

	doc = getDocInDB_freeradius(uid, collection, fields)

	if isinstance(doc, dict):
		val_ret['doc'] = doc.copy()
	else:
		val_ret['doc'] = doc

	return jsonp(request, val_ret)


def get_user_widget():
	ret = []
	
	#Jinja widget template name

	#Handlebars widget template name

	#Worker getter name

	return ret

@boxxx.post('/')
@boxxx.get('/')
def W_index():

	list_widget = get_user_widget()

	d_render = {'page_title': 'Boxxx - Configuration management tool', 'var_var': ['menu.tpl'], 'list_widget' : list_widget}

	response.content_type = 'text/html'
	OTemplate = env.get_template('index.tpl')

	return OTemplate.render(d_render)


@boxxx.route('/test')
def test():

	print request.GET.allitems()
	print request.POST.allitems()

	s = boxxx.request.environ.get('beaker.session')
	s['test'] = s.get('test',0) + 1
	s.save()

	counter_test = 'Test counter: %d' % s['test']

	d_render = {'page_title': 'Boxxx - Configuration management tool', 'counter_test': counter_test}

	response.content_type = 'text/html'
	OTemplate = env.get_template('template_content_sample.tpl')

	return OTemplate.render(d_render)


try:
	logger.info('Start Boxxx portal. Listening on http://{0}:{1}/'.format(Conf['webserver']['host'], Conf['webserver']['port']))
	boxxx.run(app=app, host=Conf['webserver']['host'], port=Conf['webserver']['port'], portal='cherrypy')	
except Exception, e:
	logger.error(u'-- Start Boxxx Portal --\n Issue into webserver: {0}\n Error stack : {1}\n'.format(e, traceback.format_exc()))
	ch.close()
	raise e