# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from time import sleep

class OtodomscraperSpider(scrapy.Spider):
    links = [f"https://www.otodom.pl/wynajem/mieszkanie/?nrAdsPerPage=72&page={i}" for i in range(101, 225)]
    name = 'otodomScraper'
    allowed_domains = ['otodom.pl']
    start_urls = links

    def __init__(self):
        
        self.options = webdriver.FirefoxOptions()
        # self.options.set_headless(True)
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--start-maximized")
        self.options.add_argument("--headless")
        # self.options.add_argument("--user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10; rv:33.0) Gecko/20100101 Firefox/33.0")
        # self.driver.add_argument("--disable-infobars")
        self.driver = webdriver.Firefox(firefox_options=self.options)
        self.driver.implicitly_wait(10)


    def parse(self, response):
        urls = response.css('div article::attr(data-url)')[3::].extract()
        for url in urls:
            self.driver.get(url)
            # self.driver.implicitly_wait(10)
            sleep(5)
            try:
                self.driver.find_elements_by_xpath("//button[@class='css-13rmyub-Button']")[0].click()
                sleep(6)
                dc = self.driver.find_element_by_xpath("//strong[@class='css-kvqyle-ShowNumber-className']").text.split(',')
                city = self.driver.find_elements_by_xpath("//a[@class='css-1sbmquw-Breadcrumb-className']")
                cname = self.driver.find_element_by_xpath("//div[@class='css-5dlbwa-AdformAccount-className']").text.split('\n')

            except Exception as e:
                pass
            
            
            yield{
                'City': city[2].text,
                'District': city[1].text,
                'Name': self.driver.find_element_by_xpath("//h1[@class='css-19829c-AdHeader-className']").text,
                'Price': self.driver.find_element_by_xpath("//div[@class='css-7ryazv-AdHeader-className']")[0].text,
                # 'Broker ID': 
                'Contact name': cname[0],
                'Contact No. 1': dc[0].replace(' ', '') if dc[0] else "Nil",
                'Contact No. 2': dc[1].replace(' ','') if len(dc) is 2 else "Nil"
            }

    