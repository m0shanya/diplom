import logging

import scrapy


class FotomagazinSpider(scrapy.Spider):
    name = "fotomagazin.by"
    allowed_domains = ["fotomagazin.by/"]
    start_urls = ["https://fotomagazin.by/foto-i-optika/fotoapparatyi/zerkalnyie-kameryi/"]

    def __init__(self, *args, **kwargs):
        logger = logging.getLogger("scrapy")
        logger.setLevel(logging.ERROR)
        super().__init__(*args, **kwargs)

    def parse(self, response, **kwargs):
        for product in response.css(".product-wrapper .product-layout .product-block .product-block-inner"):
            image_link = product.css(".product-image-block .image img::attr(src)").get()
            cost = product.css(".caption .price span").get()
            cost = cost.strip() if cost is not None and cost == '-' else 0
            data = {
                "title": product.css(".caption a::text").get().strip(),
                "cost": str(cost),
                "link": f"https://{self.allowed_domains[0]}{product.css('.caption a::attr(href)').get()}",
                "image": f"https://{self.allowed_domains[0]}{image_link}",
            }
            yield data
