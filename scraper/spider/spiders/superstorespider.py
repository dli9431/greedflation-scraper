import json
import scrapy
from datetime import date
from spider.items import ProductItem, PriceItem


class SuperstoreInitSpider(scrapy.Spider):
    name = 'init_superstore_spider'
    url = 'https://www.realcanadiansuperstore.ca/food/meat/c/27998?navid=flyout-L2-Meat'

    def start_requests(self):
        yield scrapy.Request(self.url, callback=self.parse)

    def parse(self, response):
        print(response.body)


class SuperstoreSpider(scrapy.Spider):
    name = 'superstore_spider'
    url = 'https://api.pcexpress.ca/product-facade/v3/products/category/listing'
    headers = {
        "Accept": "application/json, text/plain, */*",
        "Accept-Encoding": "gzip, deflate, br",
        "Accept-Language": "en",
        "Business-User-Agent": "PCX-Web",
        "Content-Type": "application/json",
        "Host": "api.pcexpress.ca",
        "Origin": "https://www.realcanadiansuperstore.ca",
        "Referer": "https://www.realcanadiansuperstore.ca",
        "Sec-Fetch-Dest": "empty",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Site": "cross-site",
        "Sec-GPC": "1",
        "Site-Banner": "superstore",
        "x-apikey": "1im1hL52q9xvta16GlSdYDsTsG0dmyhF",
    }

    def start_requests(self):
        payload = {
            "pagination": {"from": 0, "size": 50},
            "banner": "superstore",
            # generate this based on initial request later
            "cartId": "5d1f7722-6085-4f8e-b854-9bdd3e7d11ec",
            "lang": "en",
            "storeId": "1517",
            "pcId": None,
            "pickupType": "STORE",
            "offerType": "ALL",
            "categoryId": "27998",
        }
        yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                             headers=self.headers, cb_kwargs=dict(payload=payload))

    def parse(self, response, payload):
        data = json.loads(response.body)
        for product in data['results']:
            product_item = ProductItem(
                product_id=product['code'],
                name=product['name'],
                brand=product['brand'],
                # product_description=product['description'],
                url=product['link'],
                size=product['packageSize']
            )
            yield product_item
            price_item = PriceItem(
                product_id=product['code'],
                price=product['prices']['price']['value'],
                type=product['prices']['price']['type'],
                date=date.today()
            )
            yield price_item

        # Pagination logic
        if data['results']:  # assuming that the presence of 'results' means there's more data
            payload['pagination']['from'] += payload['pagination']['size']
            yield scrapy.Request(self.url, method='POST', body=json.dumps(payload),
                                 headers=self.headers, cb_kwargs=dict(payload=payload))