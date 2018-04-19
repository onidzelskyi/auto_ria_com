import scrapy
from urllib.parse import urlencode
from ..items import AutoRiaComItem


XPATH_LINK_ITEM = '//a[@class = "m-link-ticket"]/@href'
XPATH_CAR_IMAGE_URL = '//div[@class = "carousel"]//img/@src'

CSS_CAR_DETAILS = 'h1.head::attr("title")'
XPATH_CAR_DETAILS = '//div[@class = "box-panel description-car"]//h2[@class = "title-head inline"]/text()'


class CarSpider(scrapy.Spider):
    """Crawl car photos for shazam car."""
    name = "cars"

    """
    https://auto.ria.com/search/?categories.main.id=1&brand.id[0]=29&price.currency=1&abroad.not=-1&custom.not=-1&page=0&size=100
    https://auto.ria.com/search/?lang_id=2&page=0&countpage=50&marka_id=29&category_id=1&custom=1

    search string for mercedes
    lang_id=2 - do not change
    page=0 - do not change - we need only first 100 samples per class
    countpage=100 - # samples per page
    marka_id=48 - model for Mercedes-Benz. Get all model' ids.
    category_id=1 - passenger cars
    custom=1 - custom search

    ===
    query: categories.main.id=1&brand.id[0]=9&price.currency=1&abroad.not=-1&custom.not=-1&page=0&size=100

    ===
    params:
    categories.main.id: 1
    price.currency: 1
    abroad.not: -1
    custom.not: -1
    page: 0
    size: 100

    ===
    manufacture param:
    param name brand.id[0]
    values are:
    BMW: 84
    Volkswagen: 9
    Mercedes-Benz: 48
    Audi: 6
    Honda: 28
    Mazda: 47
    Kia: 33
    Hyundai: 29
    Toyota: 79
    Chevrolet: 13
    """

    brand_ids = {
        'BMW': 84,
        'Volkswagen': 9,
        'Mercedes-Benz': 48,
        'Audi': 6,
        'Honda': 28,
        'Mazda': 47,
        'Kia': 33,
        'Hyundai': 29,
        'Toyota': 79,
        'Chevrolet': 13,
    }

    def start_requests(self):
        urls = [
            # 'https://auto.ria.com/last/today/?',
            # 'https://auto.ria.com/legkovie/',
            'https://auto.ria.com/search/?',
        ]
        data = {
            # 'categories.main.id': 1,
            # 'price.currency': 1,
            # 'abroad.not': -1,
            # 'custom.not': -1,
            # 'page': 0,
            # 'size': 100,
            'lang_id': 2,
            'page': 0,
            'countpage': 100,
            'marka_id': 29,
            'category_id': 1,
            'custom': 1,
        }
        for brand_id in CarSpider.brand_ids.values():
            for url in urls:
                brand = {'marka_id': brand_id}
                data.update(brand)
                url = '{}{}'.format(url, urlencode(data))
                yield scrapy.Request(url=url, callback=self.parse_brand_search_page)

    def parse_brand_search_page(self, response):
        """Parse search by brand. Parse links for car items and invoke car parser for each of them."""
        for car_link in response.xpath(XPATH_LINK_ITEM):
            yield response.follow(car_link.extract(), self.parse_car_details_page)

    def parse_car_details_page(self, response):
        """Parse car details page."""
        # manufacture, model, year = response.css(CSS_CAR_DETAILS).extract_first().split()
        car_detail_items = response.xpath(XPATH_CAR_DETAILS).extract_first().split()
        manufacture = car_detail_items[1]
        model = car_detail_items[2]
        year = car_detail_items[-1]
        car_image_url = response.xpath(XPATH_CAR_IMAGE_URL).extract()

        yield AutoRiaComItem(image_urls=car_image_url,
                             # file_urls=car_image_url,
                             manufacture=manufacture,
                             model=model,
                             year=year,
                             )

    """
    def parse(self, response):
        for car in response.css('img.outline'):
            # TODO: Vehicle class
            title = car.css('img.outline::attr(title)').extract_first()
            title_items = title.split()
            # Manufacture
            # Model
            # Year
            manufacture = title_items[0]
            model = title_items[1]
            year = title_items[-1]
            yield {
                'image': car.css('img.outline::attr(src)').extract_first(),
                'manufacture': manufacture,
                'model': model,
                'year': year,
            }
            # yield AutoRiaComItem(image=image,
            #                      manufacture=manufacture,
            #                      model=model,
            #                      year=year,
            #                      )
        # next_page = response.css('a.js-next::attr(href)').extract_first()
        # if next_page is not None:
        #     yield response.follow(next_page, callback=self.parse_brand_search)
    """