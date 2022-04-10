import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_cloudflare_middleware import CloudFlareMiddleware#->ctrl+click this class #add or respose.status 429

class CryptoSpider(CrawlSpider):
    name = 'crypto'
    allowed_domains = ['coinmarketcap.com']
    start_urls = ['http://coinmarketcap.com/']

    rules = (
        Rule(LinkExtractor(restrict_xpaths="//a[@class='currency-name-container link-secondary']"), callback='parse_item', follow=True),
    )
    #https://github.com/clemfromspace/scrapy-cloudflare-middleware
    def parse_item(self, response):
        yield {
            'name': response.xpath("normalize-space((//h1[@class='details-panel-item--name']/text())[2])").get(),
            'rank': response.xpath("//span[@class='label label-success']/text()").get(),
            'price(USD)': response.xpath("//span[@class='h2 text-semi-bold details-panel-item--price__value']/text()").get()
        }