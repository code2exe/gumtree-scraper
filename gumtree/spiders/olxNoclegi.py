# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep


class OlxnoclegiSpider(scrapy.Spider):
    name = 'olxNoclegi'
    allowed_domains = ['olx.pl']
    start_urls = ['https://www.olx.pl/nieruchomosci/noclegi/']

    
    def __init__(self):
        self.options = webdriver.ChromeOptions()        
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--headless")
        # self.options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0")        
        self.driver = webdriver.Chrome(chrome_options=self.options)
        self.driver.implicitly_wait(10)
        
    def parse(self, response):
        pass
