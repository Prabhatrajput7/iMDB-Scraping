# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class BestmoviesSpider(CrawlSpider):
    name = 'bestmovies'
    allowed_domains = ['www.imdb.com']
    #start_urls = ['https://www.imdb.com/search/title/?groups=top_250&sort=user_rating']
    user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.45 Safari/537.36'

    def start_requests(self):
        yield scrapy.Request(url='https://www.imdb.com/search/title/?groups=top_250&sort=user_rating', headers={
            'User-Agent': self.user_agent#never use callback with scrapy.Requet
        })

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//h3[@class='lister-item-header']/a"), callback='parse_item', follow=True, process_request='set_user_agent'),
        Rule(LinkExtractor(restrict_xpaths='(//a[@class="lister-page-next next-page"])[1]'), process_request='set_user_agent')#not using callback here so it wont get execute first as it is a next button
        #Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
        #deny,#restrict_xpath and css
    )

    def set_user_agent(self, request):
        request.headers['User-Agent'] = self.user_agent
        return request

    def parse_item(self, response):
        #print(response.url)
        yield{
            'title': response.xpath('//div[@class="TitleBlock__TitleContainer-sc-1nlhx7j-1 jxsVNt"]/h1/text()').get(),
            'year': response.xpath('//ul[@class="ipc-inline-list ipc-inline-list--show-dividers TitleBlockMetaData__MetaDataList-sc-12ein40-0 dxizHm baseAlt"]/li[1]/a/text()').get(),
            'genre': response.xpath('//a[@class="GenresAndPlot__GenreChip-cum89p-3 fzmeux ipc-chip ipc-chip--on-baseAlt"]/span/text()').get(),
            'rating': response.xpath('(//div[@class="AggregateRatingButton__Rating-sc-1ll29m0-2 bmbYRW"])[1]/span[1]/text()').get(),
            'duration': response.xpath('normalize-space((//li[@class="ipc-inline-list__item"])[3]/text())').get(),
            'movie_url': response.url
        }