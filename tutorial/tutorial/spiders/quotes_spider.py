import scrapy
#import tldextract get only domain extract from url no matter subdomain


#list_100 : adulthood inspirational miracle miracles aliteracy deep-thoughts thinking abilities paraphrased simile

#list_50 : world success value life live books classic humor change choices love truth

class QuotesSpider(scrapy.Spider):
    name = "quotes"
    coucou = 'Vachement super'
    d_urls = {}
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

    def parse(self, response):
        page = response.url.split("/")[-2]
        link_url = response.xpath('//a/@href').extract()
        link_text = response.xpath('//a/text()').extract() #recupere tous les textes de liens
        link_textplus = response.xpath('//a/*').extract() # recupere tous ce qui n'est pas du texte mais qui dans une balise lien
        filename = 'quotes-%s.html' % page
#        yield '************\n{0}\n************'.format(link_text)
#        with open(filename, 'wb') as f:
#            f.write(response.body)
        self.log('************\n{0}\n************'.format(link_text))
        self.log('############\n{0} {1}\n############'.format(response.url, link_url))

'''
Follow link example
        if next_page is not None:
            next_page = response.urljoin(next_page)
            yield scrapy.Request(next_page, callback=self.parse)
'''
