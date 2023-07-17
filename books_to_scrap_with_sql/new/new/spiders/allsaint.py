import scrapy
from tqdm import tqdm
from scrapy.cmdline import execute


class AllsaintSpider(scrapy.Spider):
    name = "allsaint"
    allowed_domains = ["allsaints.com"]
    start_urls = ["https://www.allsaints.com/de/stores/"]

    def parse(self, response):
        j = response.xpath('//button[@class="b-accordion-button b-storelocator_locations-title"]/span/text()').get()
        sections = response.xpath('///div//div[@class="b-storelocator_locations-store"]//a/@href').getall()
        for i in tqdm(sections):
                abs_link = 'https://www.allsaints.com' + i
                yield response.follow(url=abs_link, callback=self.new_page)

    def new_page(self, response):
        opening = response.xpath('//div[@class="b-storelocator_result-schedule"]//table[1]//tr//td//text()').getall()
        store_name = response.xpath(
            '//div[@class="b-storelocator_result"]//h1[@class="b-storelocator_result-name"]/text()').get().strip()
        address = "".join(response.xpath(
            '//*[@id="maincontent"]/main/section//div[@class="b-storelocator_result-address"]/p[1]/text()').get().strip())
        phone = response.xpath('//div[@class="b-storelocator_result-phone"]//a[@class="b-link_phone"]/text()').get()
        opening_hour = {opening[i]: opening[i + 1] for i in range(0, len(opening), 2)}
        direction = response.xpath(
            '//div[@class="b-storelocator_result-actions m-one"]//a[@class="b-storelocator_result-get_directions b-button m-alt"]/@href').get()
        yield {
            "store_name": store_name,
            "address": address,
            "phone_no": phone,
            "opening_hour": opening_hour,
            "direction": direction
        }


if __name__ == '__main__':
    execute(['scrapy', 'crawl', 'allsaint'])


