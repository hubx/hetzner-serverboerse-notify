import scrapy
from hetzner.items import HetznerItem

class HetznerSpider(scrapy.Spider):
    name = "hetzner"
    allowed_domains = ["robot.your-server.de"]
    start_urls = [
        "https://robot.your-server.de/order/market/sortcol/cpu_benchmark/sorttype/up/limit/1000",
    ]

    def parse(self, response):
        a = response.css("body > div.columns > div.centercolumn > div > div")
        for b in a[11:-1]: # skip header and empty element at the end
            item = HetznerItem()
            item['id'] = b.css("table::attr(onclick)").extract()[0]
            item['cpu'] = b.css("table > tr > td.order_cpu ::text").extract()[0]
            item['cpu_b'] = b.css("table > tr > td.order_cpu_benchmark ::text").extract()[0]
            item['ram'] = b.css("table > tr > td.order_ram ::text").extract()[0][:-3]
            item['hdd'] = b.css("table > tr > td.order_hd ::text").extract()[0].strip()
            item['price'] = b.css("table > tr > td.order_price ::text").extract()[0][2:]
            item['reduction'] = b.css("table > tr > td.order_nextreduce ::text").extract()[0]
            yield item