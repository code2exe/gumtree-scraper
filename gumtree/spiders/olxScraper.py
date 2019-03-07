# -*- coding: utf-8 -*-
import scrapy


class OlxscraperSpider(scrapy.Spider):
    name = 'olxScraper'
    allowed_domains = ['olx.pl']
    start_urls = ['https://www.olx.pl/nieruchomosci/mieszkania/wynajem/']

    def parse(self, response):
        pass
