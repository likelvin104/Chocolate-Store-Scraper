import scrapy


class ChocolatespiderSpider(scrapy.Spider):
    name = "chocolatespider"
    allowed_domains = ["chocolate.co.uk"]
    start_urls = ["https://www.chocolate.co.uk/collections/all"]

    def parse(self, response):

        products = response.css('product-item')

        for product in products:
            yield{
                'name': product.css('a.product-item-meta__title::text').get(),
                'price': product.css('span.price').get().replace('<span class="price">\n              <span class="visually-hidden">Sale price</span>', '').replace('</span>', ''),
                'link': product.css('a.product-item-meta__title').attrib['href']
            }
        
        next_page = response.css("a[rel='next']")[0]
        if next_page is not None:
            yield response.follow(next_page, callback=self.parse)