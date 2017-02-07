import re
import scrapy
#import tldextract get only domain extract from url no matter subdomain

from scrapy.utils.markup import replace_tags, replace_escape_chars

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    coucou = 'Vachement super'
    d_struct_elem = {}
    d_urls = {}
    l_100 = ['adulthood', 'inspirational', 'miracle', 'miracles', 'aliteracy', 'deep-thoughts', 'thinking', 'abilities', 'paraphrased', 'simile']
    l_50 = ['world', 'success', 'value', 'life', 'live', 'books', 'classic', 'humor', 'change', 'choices', 'love', 'truth']
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

        self.log('************\n{0} {1}\n************'.format(response.url, self.d_struct_elem))

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
