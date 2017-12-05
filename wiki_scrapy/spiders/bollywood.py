# -*- coding: utf-8 -*-
import scrapy
from scrapy.selector import Selector
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from wiki_scrapy.items import BollywoodMovieItem
from wiki_scrapy.items import BollywoodPersonItem
import datetime
import itertools

class BollywoodSpider(scrapy.Spider):
    name = 'bollywood'
    allowed_domains = ['en.wikipedia.org']
    # start_urls = ['https://en.wikipedia.org/wiki/Lists_of_Bollywood_films']

    custom_settings = {
        'FEED_FORMAT' : 'json',
        'FEED_URI' : './output.json',
        'ITEM_PIPELINES' : {
            'wiki_scrapy.pipelines.BollywoodPipeline': 100
        }
    }
    
    def __init__(self, *args, **kwargs):
        super(BollywoodSpider, self).__init__(*args, **kwargs)

    def start_requests(self):
        return [scrapy.FormRequest('https://en.wikipedia.org/wiki/Lists_of_Bollywood_films', callback=self.list_of_bollywood_years)]

    def parse(self, response):
        self.logger.info('function : parse | url : %s', response.url)
        return {"error" : "parse function called"}

    def list_of_bollywood_years(self, response):
        self.logger.info('function : list_of_bollywood_years | url : %s | status : %s', response.url, response.status)
        if response.status != 200:
            return None
        self.logger.debug('status is 200 for url : %s', response.url)
        extracted_urls = response.css('a::attr(href)').extract()
        now_year = datetime.datetime.now().year
        for url in extracted_urls:
            if not url.startswith('/wiki/List_of_Bollywood_films_of_'):
                continue
            
            year = url[len('/wiki/List_of_Bollywood_films_of_'):]
            if now_year < int(year):
                continue
            
            self.logger.debug('adding another year request for url : %s', response.urljoin(url))

            yield scrapy.Request(response.urljoin(url), callback=self.bollywood_films_in_a_year)

    def bollywood_films_in_a_year(self, response):
        self.logger.info('function : bollywood_films_in_a_year | url : %s | status : %s', response.url, response.status)
        extracted_urls = response.css('tr td i a::attr(href)').extract()
        for url in extracted_urls:
            self.logger.debug('adding another film request for url : %s', response.urljoin(url))
            yield scrapy.Request(response.urljoin(url), callback=self.bollywood_film)

    def bollywood_film(self, response):
        self.logger.info('function : bollywood_film | url : %s | status : %s', response.url, response.status)
        
        item_type = 'bollywood_film'
        url = response.url
        movie_name = response.css('#firstHeading ::text').extract()[0]
        directed_by = []
        produced_by = []
        written_by = []
        release_date = None
        casts = []

        extracted_tr = response.css('tr').extract()
        for txt in extracted_tr:
            th_extracts = Selector(text=txt).xpath('//th/text()').extract()
            if len(th_extracts) == 1:
                if 'Directed by' == th_extracts[0]:
                    url_name_list = self.get_name_url_list(txt)
                    directed_by.extend(url_name_list)
                elif 'Produced by' == th_extracts[0]:
                    url_name_list = self.get_name_url_list(txt)
                    produced_by.extend(url_name_list)
                elif 'Written by' == th_extracts[0]:
                    url_name_list = self.get_name_url_list(txt)
                    written_by.extend(url_name_list)
                elif 'Starring' == th_extracts[0]:
                    url_name_list = self.get_name_url_list(txt)
                    casts.extend(url_name_list)
            else:
                th_extracts = Selector(text=txt).xpath('//th/div/text()').extract()
                if len(th_extracts) == 1:
                    if 'Release date' == th_extracts[0]:
                        release_dates = Selector(text=txt).css('.published::text').extract()
                        if len(release_dates) != 0:
                            release_date = release_dates[0]

        for url_name in itertools.chain(directed_by, produced_by, written_by, casts):
            self.logger.debug('adding another person request for url : %s', response.urljoin(url))
            yield scrapy.Request(response.urljoin(url_name['url']), callback=self.bollywood_person)

        yield BollywoodMovieItem(item_type=item_type, url=url, movie_name=movie_name, directed_by=directed_by, written_by=written_by, release_date=release_date, casts=casts)
        

    def get_name_url_list(self, html_txt):
        temp = Selector(text=html_txt).xpath('//td/a').extract()
        name_url_list = []
        for txt in temp:
            data = {
                'name' : Selector(text=txt).xpath('//text()').extract()[0],
                'url' : Selector(text=txt).xpath('//@href').extract()[0]
            }
            name_url_list.append(data)
        return name_url_list
        

    def bollywood_person(self, response):
        self.logger.info('function : bollywood_person | url : %s | status : %s', response.url, response.status)
        
        item_type = 'bollywood_person'
        url = response.url
        actor_name = response.css('#firstHeading ::text').extract()[0]
        birth_date = response.css('.bday::text').extract()
        if len(birth_date) == 0:
            birth_date = None
        else:
            birth_date = birth_date[0]
        birth_place = response.css('.birthplace').css('a::text').extract()
        if len(birth_place) == 0:
            birth_place = None
        else:
            birth_place = birth_place[0]
        nationality = None
        occupation = None
        
        extracted_tr = response.css('tr').extract()
        for txt in extracted_tr:
            th_extracts = Selector(text=txt).xpath('//th/text()').extract()
            if len(th_extracts) == 1:
                if 'Nationality' == th_extracts[0]:
                    nationality = Selector(text=txt).xpath('//td/a/text()').extract()
                elif 'Occupation' == th_extracts[0]:
                    occupation = Selector(text=txt).xpath('//td/a/text()').extract()
                    
        yield BollywoodPersonItem(item_type=item_type, url=url, actor_name=actor_name, gender=None, birth_date=birth_date, birth_place=birth_place, nationality=nationality, occupation=occupation)
