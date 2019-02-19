# -*- coding: utf-8 -*-
import scrapy



class RentSpider(scrapy.Spider):
    name = 'Rent'
    allowed_domains = ['gumtree.pl']
    start_urls = ['https://www.gumtree.pl/s-mieszkania-i-domy-do-wynajecia/v1c9008p1/']

  

    def parse(self, response):
        
        urls = response.css("div.view")[1].css("ul")[0].css("li").css("a::attr(href)").extract()
        for url in urls:
            url = response.urljoin(url)
            yield scrapy.Request(url=url, callback=self.get_details)

        # pagination links
        nxt_urls =  response.css('span.after > a::attr(href)')[0].extract()
        if nxt_urls:
        # for nxt_url in nxt_urls:
            next_urls = response.urljoin(nxt_urls)
            yield scrapy.Request(url=next_urls, callback=self.parse)

    def get_details(self, response):

        name = response.css('span.value > span::text')[0].re(r"(\d+)")
        price = "".join(name)
        num = response.css('div.usr-interactions > div > div > a::attr(href)').re(r"tel:(\d+)")
        num_s = "".join(num)
        yield {
            'City': response.css('div.location > a::text')[0].extract(),
            'District': response.css('div.location > a::text')[1].extract(),
            'Name': response.css('h1 > span.myAdTitle::text')[0].extract(),
            # 'Description': response.css('div.attribute > span.value::text')[5].extract(),
             'Price(zl)': price,
             'Broker ID': response.css('div.attribute > span.value::text')[3].extract(),
             'Contact name': response.css('span.username > a::text')[0].extract().strip(),
             'Contact number': num_s,
        }
        
        