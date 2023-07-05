from lxml import html
import requests
import mysql.connector
import re

url = "https://books.toscrape.com/catalogue/"
product_list = []
page_count = 1

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="actowiz",
    database="mytable"
)
cursor = db.cursor()

def html_parser(html_content):
    dom = html.fromstring(html_content)
    global page_count
    product_details = {
        'product_title': dom.xpath('//div[@class="col-sm-6 product_main"]//h1/text()')[0],
        'product_price': float(dom.xpath('//div[@class="col-sm-6 product_main"]//p[@class="price_color"]/text()')[0][1:]),
        'in_stock': True if re.findall(r'(In stock)+', ("".join(dom.xpath('//div[@class="col-sm-6 product_main"]//p[@class="instock availability"]/text()')).strip()))[0] == "In stock" else False,
        'image_url': url + dom.xpath('//div[@class="item active"]//@src')[0][5:],
        'stock_count': re.findall(r'\d+', ("".join(dom.xpath('//div[@class="col-sm-6 product_main"]//p[@class="instock availability"]/text()')).strip()))[0],
        'product_information': {index.xpath('.//th/text()')[0]: index.xpath('.//td/text()')[0] for index in dom.xpath('//table//tr')},
        'product_description': dom.xpath('//div[@id="product_description"]/following-sibling::p/text()')[0] if dom.xpath('//div[@id="product_description"]/following-sibling::p/text()') else "",
    }
    product_list.append(product_details)

def product_links(main_url):
    response = requests.get(main_url)
    html_content = response.content
    dom = html.fromstring(html_content)
    for href in dom.xpath('//ol/li//h3//@href'):
        page_link = requests.get(url + href)
        page_content = page_link.content
        html_parser(page_content)

while page_count < 51:
    page_url = f'https://books.toscrape.com/catalogue/page-{page_count}.html'
    print(f"page {page_count} completed")
    product_links(page_url)
    page_count += 1

for data in product_list:
    d = [
        data["product_title"],
        data["product_price"],
        data["in_stock"],
        data["image_url"],
        data["stock_count"],
        str(data["product_information"]),
        data["product_description"]
    ]
    query = "INSERT INTO mytable (product_title, product_price, in_stock, image_url, stock_count, product_information, product_description) VALUES (%s, %s, %s, %s, %s, %s, %s)"
    cursor.execute(query, d)

db.commit()
