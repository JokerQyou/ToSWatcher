# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class TwitterSpider(scrapy.Spider):
    name = 'twitter'
    allowed_domains = ['twitter.com']
    start_urls = [
        # Twitter ToS
        'https://twitter.com/en/tos',
        # Twitter Privacy policy
        'https://twitter.com/en/privacy',
    ]

    def parse(self, response):
        soup = BeautifulSoup(
            response.css('body div#main-content')[0].get(), 'lxml'
        )
        yield {
            'title': response.css('body h1::text').extract_first(),
            'text': soup.get_text(),
            'url': response.url,
        }
