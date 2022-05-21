import scrapy
from scrapy.selector import Selector
import time

class TrovitcrawlerSpider(scrapy.Spider):
    name = 'TrovitCrawler'

    # allowed_domains = ['www.homes.trovit.com']

    def start_requests(self):
        start_urls = ["https://homes.trovit.com/index.php/cod.search_homes/type.1/what_d.ca/sug.0/isUserSearch.1/order_by.source_date/geo_id.R165475/"]
        self.pages = 5
        self.current = 1
        for url in start_urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for item in response.xpath("//div[@class='snippet-wrapper js-item-wrapper']"):
            yield {
                'title': item.xpath(".//div[@class='item-title']/span/text()").get(),
                'price': self.correct_price(item.xpath(".//span[@class='actual-price']/text()").get()),
                'link': item.xpath(".//a[@class='rd-link']").attrib['href'],
                'publish_time': item.xpath(".//span[@class='item-published-time']/text()").get(),
                'address': item.xpath(".//span[@class='address ']/text()").get().strip()
            }
        if self.current != self.pages:
            
            next_url = response.xpath('//a[@data-test="p-next"]').attrib['href']
            if next_url is not None:
                time.sleep(5)
                yield scrapy.Request(url=next_url, callback=self.parse)
                self.current += 1



    @staticmethod
    def correct_price(raw_price):
        np = ''
        nums = '1234567890.'
        for char in raw_price:
            if char in nums:
                np += char
        return np
