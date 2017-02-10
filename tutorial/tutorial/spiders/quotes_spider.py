import re
import scrapy
#import tldextract get only domain extract from url no matter subdomain
#import chardet detect encoding

from scrapy.utils.markup import replace_tags, replace_escape_chars

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    coucou = 'Vachement super'
    d_struct_elem = {}
    d_urls = {}
    l_100 = ['adulthood', 'inspirational', 'miracle', 'miracles', 'aliteracy', 'deep-thoughts', 'thinking', 'abilities', 'paraphrased', 'simile']
    l_50 = ['world', 'success', 'value', 'life', 'live', 'books', 'classic', 'humor', 'change', 'choices', 'love', 'truth', 'milk', 'parc']
    l_100_complex = ['adulthood is a miracle']
    l_50_complex = ['world of success']
    l_black_list = []

    def start_requests(self):
        urls = [
            'http://nepi-vtudev.neuilly.ratp/test_scrapy.html',
            'http://grosincidents-dev.neuilly.ratp',
            'http://atlas.neuilly.ratp/',
            'http://grr.neuilly.ratp',
            'http://tdbcg-dev.neuilly.ratp',
            'http://segyka-dev.neuilly.ratp'
        ]
        self.log('GROSSE INFO {0}'.format(self.coucou))
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def remove_html_tags(self, data):
        ret = replace_tags(data, token=' ')
        ret = replace_escape_chars(ret)
        ret = re.sub(' {2,}', ' ', ret)

#        ret = re.sub('\\\t|\\n|\\t|\\r| {2,}', ' ', ret)

 #       self.log('$$$$$$$$$$$$$$\n{0}\n$$$$$$$$$$$$$$'.format(type(ret)))

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
                self.log('************\n{0}\n************'.format(weight))

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
                self.log('************\n{0}\n************'.format(weight))

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
        l_100_in_text = set(self.l_100)
        l_50_in_text = set(self.l_50)
        weight = 0
###
# Mettre regexp pour match approx du mot
###
        for elem in l_elem:
            for split_elem in elem.split(' '):
                split_elem = split_elem.lower()
                if split_elem in l_100_in_text :
                    weight += 100
                elif split_elem in l_50_in_text:
                    weight += 50

#        self.log('************\n{0} {1}\n************'.format(weight, l_elem))
        return weight

    def calc_wght_struct(self):
        l_elem_struct = [{'elem': 'h1', 'factor': 1.8}, {'elem': 'h2', 'factor': 1.7}, {'elem': 'h3', 'factor': 1.6}, {'elem': 'h4', 'factor': 1.5}, {'elem': 'h5', 'factor': 1.4}, {'elem': 'h6', 'factor': 1.3}, {'elem': 'li', 'factor': 1.5}, {'elem': 'td', 'factor': 1.5}, {'elem': 'th', 'factor': 1.5}, {'elem': 'title', 'factor': 1.9}, {'elem': 'select', 'factor': 1.7}, {'elem': 'meta', 'factor': 1.8}]
        weight = 0

        for struct in l_elem_struct:
            c_weight = self.calc_wght(self.d_struct_elem[struct['elem']])
            if c_weight != 0:
                weight += c_weight * struct['factor']

        return weight

    def calc_wght_link(self):
        #l_elem_link = ['link_url', 'link_text']
        #2
        #1.8
        #1.5
        #'toto[ \-_]?titi[ \-_]?tutu'
        pass

    def parse(self, response):
        page = response.url.split("/")[-2]

        self.d_struct_elem['link_url'] = response.xpath('//a/@href').extract()
#        link_text = response.xpath('//a/text()').extract() #recupere tous les textes de liens
        self.d_struct_elem['link_text'] = response.xpath('//a/*|//a/text()').extract() # recupere tous ce qui dans la balise texte ou pas
        
        self.d_struct_elem['h1'] = response.xpath('//h1/text()|//h1/*').extract()

        self.d_struct_elem['h2'] = response.xpath('//h2/text()|//h2/*').extract()

        self.d_struct_elem['h3'] = response.xpath('//h3/text()|//h3/*').extract()

        self.d_struct_elem['h4'] = response.xpath('//h4/text()|//h4/*').extract()

        self.d_struct_elem['h5'] = response.xpath('//h5/text()|//h5/*').extract()

        self.d_struct_elem['h6'] = response.xpath('//h6/text()|//h6/*').extract()

        self.d_struct_elem['li'] = response.xpath('//li/text()|//li/*').extract()
        self.d_struct_elem['td'] = response.xpath('//td/text()|//td/*').extract()
        self.d_struct_elem['th'] = response.xpath('//th/text()|//th/*').extract()

        body = response.xpath('//body').extract()
        #['body'] = body[0].encode('utf8')
        self.d_struct_elem['body'] = body

        title = response.xpath('//title/text()|//title/*').extract()
        self.d_struct_elem['title'] = title

        self.d_struct_elem['select'] = response.xpath('//option/@value|//option/text()').extract()

        self.d_struct_elem['meta'] = response.xpath('//meta[@name="description"]/@content|//meta[@name="keywords"]/@content').extract()

        l_keys = self.d_struct_elem.keys()

        for key in l_keys:
            l_value_wo_html_tag = []
            for value in self.d_struct_elem[key]:
                l_value_wo_html_tag.append(self.remove_html_tags(value))
            self.d_struct_elem[key] = l_value_wo_html_tag

#        self.log('************\n{0} {1}\n************'.format(response.url, self.d_struct_elem))

        wght_text = self.calc_wght_text()
        wght_struct = self.calc_wght_struct()
        wght_link = self.calc_wght_link()

        self.log('************\n{0} {1}\n************'.format(response.url, wght_text))

'''
        if select :
            self.log('************\n{0} {1}\n************'.format(response.url, select))

        

        find = re.search('truth', body)

        if find:
            self.log('************\n{0} {1}\n************'.format(response.url, find.group(0)))

        body = remove_tags(body)

#####
## <meta name="description" content="Free Web tutorials">
## <meta name="keywords" content="HTML,CSS,XML,JavaScript">
#####
        


        self.log('############\n{0}\n############'.format(meta))

        filename = 'quotes-%s.html' % page
'''
#       yield '************\n{0}\n************'.format(link_text)
#        with open(filename, 'wb') as f:
#            f.write(body.encode('utf8'))
#        self.log('************\n{0}\n************'.format(body))
#        self.log('############\n{0} {1}\n############'.format(response.url, link_url))

'''
Follow link example
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
'''
