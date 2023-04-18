import scrapy
from ChocolateScraper.items import ChocolateProduct
from ChocolateScraper.itemloaders import ChocolateProductLoader

class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):

        products = response.css('product-item')

        for product in products:
            chocolate = ChocolateProductLoader(item=ChocolateProduct(), selector=product)
            chocolate.add_css('name', 'a.product-item-meta__title::text')
            chocolate.add_css('price', 'span.price', re='<span class="price">\n              <span class="visually-hidden">Sale price</span>(.*)</span>')
            chocolate.add_css('url', 'a.product-item-meta__title::attr(href)')
            yield chocolate.load_item()
        
        next_page = response.css("a[rel='next']")[0]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)