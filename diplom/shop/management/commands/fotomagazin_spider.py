import logging
from pathlib import Path
from django.core.management.base import BaseCommand


import requests
from decimal import Decimal
from django.conf import settings
from shop.models import Product, Category
from shop.spiders import FotomagazinSpider
from scrapy import signals
from scrapy.signalmanager import dispatcher
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = "Crawl Fotomagazin catalog"

    def handle(self, *args, **options):
        def crawler_results(signal, sender, item, response, spider):
            item["cost"] = Decimal(item["cost"])
            if item["image"]:
                response = requests.get(item["image"])
                if response.ok:
                    path = Path(item["image"])
                    with open(settings.MEDIA_ROOT / path.name, "wb") as f:
                        f.write(response.content)
                    item["image"] = path.name
            Product.objects.create(
                image=item["image"],
                title=item["title"],
                description=item["title"],
                link=item["link"],
                category=Category.objects.first(),
                cost=item["cost"],
            )

        dispatcher.connect(crawler_results, signal=signals.item_scraped)

        process = CrawlerProcess(get_project_settings())
        process.crawl(FotomagazinSpider)
        process.start()
