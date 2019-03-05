# -*- coding: utf-8 -*-
import scrapy
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
from time import sleep



# class OtodomSpider(scrapy.Spider):
#     name = 'otodom'
#     allowed_domains = ['otodom.pl']
#     start_urls = ['https://www.otodom.pl/wynajem/mieszkanie/']

#     def __init__(self, *args, **kwargs):
#         self.options = webdriver.ChromeOptions()
#         # self.options.set_headless(True)
#         self.options.add_argument("--window-size=1920,1080")
#         self.options.add_argument("--start-maximized")
#         self.options.add_argument("--headless")
#         self.driver = webdriver.Chrome(chrome_options=self.options)
        
#         super(OtodomSpider, self).__init__(*args, **kwargs)

#     def parse(self, response):
#         urls = response.css('div article::attr(data-url)')[3::].extract()
#         # while True:
#         for url in urls:
#             self.driver.get(url)
#             sleep(1)
#             self.driver.find_element_by_xpath("//button[@class='css-13rmyub-Button']").click()
#             sleep(5)
#             x = self.driver.find_element_by_xpath("//strong[@class='css-kvqyle-ShowNumber-className']").text
#             # po of private offer
#             # po = self.driver.find_element_by_xpath("//h6[@class='box-contact-info-type w400']").text
#             # 2po
#             # poii = self.driver.find_element_by_xpath("")


            # yield {
            #     'City': self.driver.find_element_by_xpath("//p[@class='address-links']/a[3]").text,
            #     'Name': self.driver.find_element_by_xpath("//h1[@itemprop='name']").text,
            #     'District': self.driver.find_element_by_xpath("//p[@class='address-links']/a[2]").text,
            #     'Price': self.driver.find_element_by_xpath("//div[@class='css-7ryazv-AdHeader-className']").text,
            #     # 'Broker ID': 
            #     'Contact name': self.driver.find_element_by_xpath("//span[@itemprop='name']").text,
            #     'Contact number': x.replace(' ', ''),
            # }
            # # 'tags': [e.text for e in quote.find_elements_by_class_name('tag')]
class OtodomscraperSpider(scrapy.Spider):
    name = 'otodomScraper'
    allowed_domains = ['otodom.pl']
    start_urls = ['https://www.otodom.pl/wynajem/mieszkanie/?nrAdsPerPage=72&page=101']

    def __init__(self):
        # self.prox = Proxy()
        # self.prox.proxy_type = ProxyType.MANUAL
        # self.prox.http_proxy = "127.0.0.1:24000"
        # self.prox.socks_proxy = "127.0.0.1:24000"
        # self.prox.ssl_proxy = "127.0.0.1:24000"
        # self.capab = webdriver.DesiredCapabilities.FIREFOX
        # self.prox.add_to_capabilities(self.capab)
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
                city = self.driver.find_elements_by_xpath("//a[@class='css-1yn9dg6-Breadcrumb-className']")
                cname = self.driver.find_element_by_xpath("//div[@class='css-5dlbwa-AdformAccount-className']").text.split('\n')

            except Exception as e:
                pass
            
            
            yield{
                'City': city[2].text,
                'District': city[1].text,
                'Name': self.driver.find_element_by_xpath("//h1[@class='css-19829c-AdHeader-className']").text,
                'Price': self.driver.find_element_by_xpath("//div[@class='css-7ryazv-AdHeader-className']").text,
                # 'Broker ID': 
                'Contact name': cname[0],
                'Contact No. 1': dc[0].replace(' ', '') if dc[0] else "Nil",
                'Contact No. 2': dc[1].replace(' ','') if len(dc) is 2 else "Nil"
            }
        
        for i in range(102, 225):
            ht = f'https://www.otodom.pl/wynajem/mieszkanie/?nrAdsPerPage=72&page={i}'
            yield scrapy.Request(url=ht, callback=self.parse, dont_filter=True)
    