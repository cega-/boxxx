import logging
import os
import re
import scrapy
#import tldextract get only domain extract from url no matter subdomain
#import chardet detect encoding

from scrapy.utils.log import configure_logging
from scrapy.utils.markup import replace_tags, replace_escape_chars

class BoxxxSpider(scrapy.Spider):
	name = "Boxxx Crawl"
	coucou = 'Vachement super'
	d_struct_elem = {}
	d_urls = {}
	l_100 = []
	l_100_complex = []
	l_50 = []
	l_50_complex = []
#	l_100 = ['adulthood', 'inspirational', 'miracle', 'miracles', 'aliteracy', 'deep-thoughts', 'thinking', 'abilities', 'paraphrased', 'simile']
#	l_50 = ['world', 'success', 'value', 'life', 'live', 'books', 'classic', 'humor', 'change', 'choices', 'love', 'truth', 'milk', 'parc']
#	l_100_complex = ['adulthood is a miracle']
#	l_50_complex = ['world of success']
	d_black_list = {}
	d_suspicious_list = {}
	urls = {}
	l_new_domain_to_explore = []
	l_url_already_parse = []
	d_domain_abstract_weight = {}

	configure_logging(install_root_handler=False)
	logging.basicConfig(
		filename='boxxx_website_blacklist_indexer.scrapy.log',
		format='%(asctime)s - %(name)s - %(levelname)s: %(message)s',
		level=logging.INFO
	)

	def insert_in_url_to_parse(self, website):
		self.urls[str(os.urandom(16))] = {'parent': None, 'link': website, 'level': 0}

	def init_list_data_from_file(self, filename):
		l_list = []

		fd = open(filename, 'r')

		for line in fd:
			l_list.append(line[:-1])

		return l_list

	def start_requests(self):
#        urls = [
#            'http://nepi-vtudev.neuilly.ratp/test_scrapy.html',
#            'http://grosincidents-dev.neuilly.ratp',
#            'http://atlas.neuilly.ratp/',
#            'http://grr.neuilly.ratp',
#            'http://tdbcg-dev.neuilly.ratp',
#            'http://segyka-dev.neuilly.ratp'
#        ]
#		urls = [
#			'http://nepi-vtudev.neuilly.ratp/test_scrapy.html'
#		]
#		d_url_info = {}

#		d_url_info['parent'] = None
#		d_url_info['link'] = 'http://nepi-vtudev.neuilly.ratp/test_scrapy.html'
#		d_url_info['level'] = 0

		self.log('\n\n** ---- INIT Spider data ---- **\n\n'.format())

		self.l_100 = self.init_list_data_from_file('l_100.list')
		self.l_50 = self.init_list_data_from_file('l_50.list')
		self.l_100_complex = self.init_list_data_from_file('l_100_complex.list')
		self.l_50_complex = self.init_list_data_from_file('l_50_complex.list')

		for website in self.init_list_data_from_file('l_website.list'):
			self.insert_in_url_to_parse(website)

		for key, d_url in self.urls.iteritems():
			self.log('\n\n** --- SEND New URL to parse {0} ---- **\n\n'.format(d_url))

			request = scrapy.Request(url=d_url['link'], callback=self.parse)
			request.meta['d_url'] = d_url
			request.meta['key'] = key
			yield request

	def remove_html_tags(self, data):
		ret = replace_tags(data, token=' ')
		ret = replace_escape_chars(ret)
		ret = re.sub(' {2,}', ' ', ret)
		return ret.strip()

	def calc_wght_text(self):
		body = self.d_struct_elem['body'][0]
		l_text_words = body.split()
		nb_word_in_text = 0
		nb_word_in_l_50 = 0
		nb_word_in_l_100 = 0
		weight = 0
			
		l_100_in_text = set(self.l_100)
		l_50_in_text = set(self.l_50)

		for complex_100 in self.l_100_complex:
			complex_100 = complex_100.split(' ')
			s_regexp = ''
			length = len(complex_100)
			for word in complex_100:
				length -= 1
				if length:
					s_regexp += word+'[ \-_]?'
				else:
					s_regexp += word
			find_complex_100 = re.findall(s_regexp, body)
			if find_complex_100:
				weight += 100 * len(find_complex_100)
#                self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('body', 'complex_100', weight))

		for complex_50 in self.l_50_complex:
			complex_50 = complex_50.split(' ')
			s_regexp = ''
			length = len(complex_50)
			for word in complex_50:
				length -= 1
				if length:
					s_regexp += word+'[ \-_]?'
				else:
					s_regexp += word
			find_complex_50 = re.findall(s_regexp, body)
			if find_complex_50:
				weight += 50 * len(find_complex_50)
#                self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('body', 'complex_50', weight))

		for word in l_text_words:
			word = word.lower()
			if word in l_100_in_text :
				weight += 100
				nb_word_in_l_100 += 1
			elif word in l_50_in_text:
				weight += 50
				nb_word_in_l_50 += 1
			nb_word_in_text += 1

		if 100*(nb_word_in_l_100+nb_word_in_l_50)/nb_word_in_text >= 10 or nb_word_in_text <= 100:
			return weight
		else :
			return 0 

	def calc_wght(self, l_elem):
		weight = 0
###
# Mettre regexp pour match approx du mot
###
		for elem in l_elem:
			ret_complex_wght = self.calc_wght_complex(elem)
			if ret_complex_wght:
				weight += ret_complex_wght
			else:
				weight += self.calc_wght_simple(elem)

#        self.log('\n************\n{0} {1}\n************'.format(weight, l_elem))
		return weight

	def find_simple_term(self, elem):
		l_100_in_text = set(self.l_100)
		l_50_in_text = set(self.l_50)

		if elem in l_100_in_text :
			return 100, elem
		if elem in l_50_in_text :
			return 50, elem

		return None

	def calc_wght_simple(self, elem):
		weight = 0

		for split_elem in elem.split(' '):
			split_elem = split_elem.lower()
			ret_find_simple_term = self.find_simple_term(split_elem)
			if ret_find_simple_term :
				weight += ret_find_simple_term[0]

		return weight

	def calc_wght_complex(self, elem):
		weight = 0

		find_complex_50 = self.find_complex_50_term(elem)

		if find_complex_50:
			weight += 50 * len(find_complex_50[0])
		else :

			find_complex_100 = self.find_complex_100_term(elem)
			if find_complex_100:
				weight += 100 * len(find_complex_100[0])

		return weight

	def find_complex_50_term(self, elem):

		for complex_50 in self.l_50_complex:
			match_complex_50_term = complex_50
			complex_50 = complex_50.split(' ')
			s_regexp = ''
			length = len(complex_50)
			for word in complex_50:
				length -= 1
				if length:
					s_regexp += word+'[ \-_]?'
				else:
					s_regexp += word
			find_complex_50 = re.findall(s_regexp, elem)
			if find_complex_50:
				return find_complex_50, match_complex_50_term

		return None

	def find_complex_100_term(self, elem):

		for complex_100 in self.l_100_complex:
			match_complex_100_term = complex_100
			complex_100 = complex_100.split(' ')
			s_regexp = ''
			length = len(complex_100)
			for word in complex_100:
				length -= 1
				if length:
					s_regexp += word+'[ \-_]?'
				else:
					s_regexp += word
			find_complex_100 = re.findall(s_regexp, elem)
			if find_complex_100:
				return find_complex_100, match_complex_100_term

		return None

	def calc_wght_struct(self):
		l_elem_struct = [{'elem': 'h1', 'factor': 1.8}, {'elem': 'h2', 'factor': 1.7}, {'elem': 'h3', 'factor': 1.6}, {'elem': 'h4', 'factor': 1.5}, {'elem': 'h5', 'factor': 1.4}, {'elem': 'h6', 'factor': 1.3}, {'elem': 'li', 'factor': 1.5}, {'elem': 'td', 'factor': 1.5}, {'elem': 'th', 'factor': 1.5}, {'elem': 'title', 'factor': 1.9}, {'elem': 'select', 'factor': 1.7}, {'elem': 'meta', 'factor': 1.8}]
		weight = 0

		for struct in l_elem_struct:
			c_weight = self.calc_wght(self.d_struct_elem[struct['elem']])
			if c_weight != 0:
				weight += c_weight * struct['factor']
#                self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format(struct['elem'], struct['factor'], weight))

		return weight

	def weight_4_type_of_link(self, match_term, d_link):
		weight = 0

		if match_term and re.findall('[/=?&]{0}[/=?&\r\n]'.format(match_term[1]), d_link['url']):
			weight += 2 * match_term[0]
#            self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('TAG', match_term[1], match_term[0]))
		elif match_term and re.findall('[/=?&].*{0}.*[/=?&]*'.format(match_term[1]), d_link['url']):
			weight += 1.8 * match_term[0]
#            self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('LINK', match_term[1], match_term[0]))
		elif match_term:
			weight += 1.5 * match_term[0]

		return weight

	def find_weight_level_4_link(self, d_link):

		s_regexp = ''
		weight = 0
		is_complex = True

		match_term = self.find_complex_50_term(d_link['text'])

		if match_term:
			match_term = list(match_term)
			match_term[0] = 50
		elif not match_term :
			match_term = self.find_complex_100_term(d_link['text'])
			if match_term:
				match_term = list(match_term)
				match_term[0] = 100

		if not match_term :
			for split_elem in d_link['text'].split(' '):
				split_elem = split_elem.lower()
#                self.log('\n************\nWhere:{0} Which:{1} \n************'.format('Link Text', split_elem))
				match_term = self.find_simple_term(split_elem)
				if match_term:
					weight += self.weight_4_type_of_link(match_term, d_link)
#                    self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('link', match_term[1], match_term[0]))
			is_complex = False
			

#        if match_term:
#            self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('link', match_term[1], match_term[0]))

		if is_complex and match_term:
			match_term = list(match_term)
			l_word = match_term[1]
			l_word = l_word.split(' ')
			length = len(l_word)
			for word in l_word:
				length -= 1
				if length:
					s_regexp += word+'[ \-_]?'
				else:
					s_regexp += word
			match_term[1] = s_regexp
			weight += self.weight_4_type_of_link(match_term, d_link)
#            self.log('\n************\nWhere:{0} Which:{1} Weight:{2}\n************'.format('link', match_term[1], match_term[0]))

		return weight

	def calc_wght_link(self):
		weight = 0
		
#        self.log('\n::: {0} :::\n'.format(len(self.d_struct_elem['link'])))    

		for i in range(0, len(self.d_struct_elem['link'])):
			weight += self.find_weight_level_4_link(self.d_struct_elem['link'][i])
#            self.log('\n::: {1} <--> {0} :::\n'.format(self.d_struct_elem['link'][i]['url'], self.d_struct_elem['link'][i]['text']))

		return weight

	def parse_link_join_text_url(self):

		l_all_link_in_page = self.d_struct_elem['link']

		self.d_struct_elem['link'] = []

		for link in l_all_link_in_page:
			link = replace_escape_chars(link)
			link = re.sub(' {2,}', ' ', link)
			match_group_in_link = re.findall('(href=[\"\'])([^\"]*)([^>]*)>(.*)</a>', link)
			link_split = match_group_in_link[0]
			link_split = list(link_split)
			link_split[3] = replace_tags(link_split[3], token='')
			self.d_struct_elem['link'].append({'url': link_split[1], 'text': link_split[3]})
#            self.log('\n::: {0} \n {1} :::\n'.format(link_split, link))


	def is_current_domain(self, current_page, link):
		page = link.split("/")
		http = page[0]

#		self.log('\n\n** --- URL SPLIT {0} ---- **\n\n'.format(page))

		try:
			page = '//'.join([page[0], page[2]])
		except Exception, e:
			page = '//'.join([page[0], page[1]])
			pass
		
#		self.log('\n\n** --- HTTP {0} - {1} ---- **\n\n'.format(link, page))

		if page == current_page:
			return True
		elif not http : 
			return True
		else:
			return False

	def insert_into_new_domain_to_explore(self, d_url):
		already_in = False

		for domain in self.l_new_domain_to_explore:
			if domain['domain'] == d_url['domain']:
				already_in = True
				break
		
		if not already_in:
			self.l_new_domain_to_explore.append({'parent': d_url['parent'], 'link': d_url['link'], 'level': d_url['level'], 'domain': d_url['domain']})

	def get_new_domain_to_explore(self):
		l_domain = []

		for domain in self.l_new_domain_to_explore:
			if self.in_blacklist(domain['parent']):
				l_domain.append(domain)

		return l_domain

	def in_blacklist(self, page):
		if page in self.d_black_list.keys():
			return True
		else:
			return False

	def insert_in_black_list(self, page, weight):
		nbr_entry_in_black_list = 0
		weight = 0

		for page, page_info in self.d_black_list.iteritems():
			nbr_entry_in_black_list +=1
			weight += page_info['weight']

		if weight:
			global_black_list_average_weight = weight / nbr_entry_in_black_list
		else:
			global_black_list_average_weight = 0

		if weight >= global_black_list_average_weight:
			self.d_black_list[page] = {'weight': weight}
		elif weight >= global_black_list_average_weight*0.7 and weight < global_black_list_average_weight:
			self.d_black_list[page] = {'weight': weight}
		elif weight >= global_black_list_average_weight*0.4 and weight < global_black_list_average_weight*0.7:
			self.d_suspicious_list[page] = {'weight': weight}
		elif weight < global_black_list_average_weight*0.4:
			#Nothing todo
			pass

		return

	def parse(self, response):

		d_url = response.meta['d_url']

		self.log('\n\n** --- CURRENTLY Parse {0} ---- **\n\n'.format(d_url))

		page = response.url.split("/")
		page = '//'.join([page[0], page[2]])
		
		if page not in self.d_domain_abstract_weight.keys():
			self.d_domain_abstract_weight[page] =  {'nbr_page': 0, 'sum_wght': 0}
		
		self.l_url_already_parse.append(response.url)
		self.d_domain_abstract_weight[page]['nbr_page'] += 1

		self.d_struct_elem['link'] = response.xpath('//a').extract()

		self.parse_link_join_text_url()

		self.d_struct_elem['link_url'] = response.xpath('//a/@href').extract()
		
		self.d_struct_elem['h1'] = response.xpath('//h1/text()|//h1/*').extract()

		self.d_struct_elem['h2'] = response.xpath('//h2/text()|//h2/*').extract()

		self.d_struct_elem['h3'] = response.xpath('//h3/text()|//h3/*').extract()

		self.d_struct_elem['h4'] = response.xpath('//h4/text()|//h4/*').extract()

		self.d_struct_elem['h5'] = response.xpath('//h5/text()|//h5/*').extract()

		self.d_struct_elem['h6'] = response.xpath('//h6/text()|//h6/*').extract()

		self.d_struct_elem['li'] = response.xpath('//li/text()|//li/*').extract()
		self.d_struct_elem['td'] = response.xpath('//td/text()|//td/*').extract()
		self.d_struct_elem['th'] = response.xpath('//th/text()|//th/*').extract()

		#body = response.xpath('//body').extract()
		#['body'] = body[0].encode('utf8')
		self.d_struct_elem['body'] = response.xpath('//body').extract()

		title = response.xpath('//title/text()|//title/*').extract()
		self.d_struct_elem['title'] = title

		self.d_struct_elem['select'] = response.xpath('//option/@value|//option/text()').extract()

		self.d_struct_elem['meta'] = response.xpath('//meta[@name="description"]/@content|//meta[@name="keywords"]/@content').extract()

		l_keys = self.d_struct_elem.keys()

#        self.log('\n************\n{0}\n************'.format(self.d_struct_elem['link_text']))

		for key in l_keys:
			l_value_wo_html_tag = []
			for value in self.d_struct_elem[key]:
				if isinstance(value, unicode) or isinstance(value, str) :
					string_with_only_whitespace = re.findall('^[ \t\n]*$', value)
					if not string_with_only_whitespace:
						l_value_wo_html_tag.append(self.remove_html_tags(value))
			if key != 'link':
				self.d_struct_elem[key] = l_value_wo_html_tag

#        self.log('\n************\n{0}\n************'.format(self.d_struct_elem['link_text']))

#        self.log('\n************\n{0} {1}\n************'.format(response.url, self.d_struct_elem))

		wght_text = self.calc_wght_text()
		wght_struct = self.calc_wght_struct()
#        self.log('\n::: {0} \n :::\n'.format(self.d_struct_elem['link']))
		wght_link = self.calc_wght_link()

		self.d_domain_abstract_weight[page]['sum_wght'] += wght_text + wght_struct + wght_link

#		self.log('\n************\n{0} {1}\n************'.format(response.url, wght_link))
		self.log('\n************\n{0} {1}\n************'.format(page, wght_link))

		for link in self.d_struct_elem['link_url'] :
			if link not in self.l_url_already_parse:
				d_url_info = {}
				if d_url['level'] <= 2 and self.is_current_domain(page, link):
					d_url_info['parent'] = page
					d_url_info['link'] = link
					d_url_info['level'] = d_url['level'] + 1
					request = scrapy.Request(url=response.urljoin(link), callback=self.parse)
					request.meta['d_url'] = d_url_info
					request.meta['key'] = key
					yield request
				elif not self.is_current_domain(page, link):
					domain = link.split("/")
					domain = '//'.join([domain[0], domain[2]])
					d_url_info['parent'] = page
					d_url_info['domain'] = domain
					d_url_info['link'] = link
					d_url_info['level'] = 0
					self.log('\n************\n{0} {1}\n************'.format('To Other Domain', link))
					self.insert_into_new_domain_to_explore(d_url_info)
				elif d_url['level'] >= 3 and self.in_blacklist(page) == False:
#					pass
					average_wght = self.d_domain_abstract_weight[page]['sum_wght'] / self.d_domain_abstract_weight[page]['nbr_page']
					self.log('\n************\n{0} {1}\n************'.format('Average weight', average_wght))
					self.insert_in_black_list(page, average_wght)
					## Calc to insert in black list ##
					## if ok add in black list ##

		for new_domain in self.get_new_domain_to_explore():
			request = scrapy.Request(url=new_domain['link'], callback=self.parse)
			request.meta['d_url'] = new_domain
			request.meta['key'] = key
			yield request
