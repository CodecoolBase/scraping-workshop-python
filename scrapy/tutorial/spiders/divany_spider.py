import scrapy
import json
from scrapy.loader import ItemLoader
from tutorial.items import ArticleItem


class DivanySpider(scrapy.Spider):
    name = "divany"

    def start_requests(self):
        urls = [
            'https://divany.hu/szuloseg/'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for article in response.css('a.c-anyag-horizontalis_text_title'):
            article_link = article.css('a::attr(href)').extract_first()

            a = ItemLoader(item=ArticleItem(), response=response)
            a.add_value( 'title', article.css('::text').extract_first() )
            a.add_value( 'link', article_link )

            request = scrapy.Request(url="https://graph.facebook.com/?ids=" + article_link, callback=self.parse_facebook)
            request.meta['item'] = a
            yield request
    
    def parse_facebook(self, response):
        a = response.meta['item']
        share_count = response.xpath('string(//body)').re(r'\"share_count\": (\d+)')
        a.add_value( 'fb_share_count', share_count )
        yield a.load_item()
