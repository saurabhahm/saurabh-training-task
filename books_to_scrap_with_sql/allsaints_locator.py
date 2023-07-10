import requests
from lxml import html
import pandas as pd
from tqdm import tqdm

store_data = list()

def extractor(abs_link, country):
    response = requests.get(abs_link)
    obj = html.fromstring(response.content)
    opening = obj.xpath('//div[@class="b-storelocator_result-schedule"]//table[1]//tr//td//text()')
    data = {
        "country": country,
        "store_name":
            obj.xpath('//div[@class="b-storelocator_result"]//h1[@class="b-storelocator_result-name"]/text()')[
                0].strip(),
        "address": " ".join(
            obj.xpath('//*[@id="maincontent"]/main/section//div[@class="b-storelocator_result-address"]/p[1]/text()')),
        "phone": obj.xpath('//div[@class="b-storelocator_result-phone"]//a[@class="b-link_phone"]/text()')[0],
        "opening_hour": {opening[i]: opening[i + 1] for i in range(0, len(opening), 2)},
        "direction": obj.xpath(
            '//div[@class="b-storelocator_result-actions m-one"]//a[@class="b-storelocator_result-get_directions b-button m-alt"]/@href')[
            0]
    }
    store_data.append(data)


url = "https://www.allsaints.com/de/stores/"
response = requests.get(url)
obj = html.fromstring(response.content)
j = obj.xpath('//button[@class="b-accordion-button b-storelocator_locations-title"]/span/text()')
for index, link in tqdm(enumerate(obj.xpath('//section[@data-widget="accordionItem"]'))):
    for i in link.xpath('.//a/@href'):
        abs_link = 'https://www.allsaints.com' + i
        extractor(abs_link, j[index])

for i in store_data:
    print(i)
df = pd.DataFrame(store_data)
df.to_json("store_data.json", orient='records')
