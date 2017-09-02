# -*- coding: utf-8 -*-
import scrapy
from bs4 import BeautifulSoup


class TaobaoSpider(scrapy.Spider):
    name = 'taobao'
    allowed_domains = ['taobao.com', 'alicdn.com']
    start_urls = [
        # 淘宝平台服务协议
        'http://terms.alicdn.com/legal-agreement/terms/TD/TD201609301342_19559.html',  # noqa
        # 法律声明及隐私权政策
        'http://terms.alicdn.com/legal-agreement/terms/suit_bu1_taobao/suit_bu1_taobao201703241622_61002.html',  # noqa
    ]

    def parse(self, response):
        soup = BeautifulSoup(response.css('body')[0].get(), 'lxml')
        tos_content = soup.get_text().replace('\xa0', '\n')
        yield {
            'title': response.css('body span::text').extract_first(),
            'text': tos_content,
            'url': response.url,
        }
