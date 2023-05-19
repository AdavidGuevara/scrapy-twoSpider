import scrapy


class NewcarSpider(scrapy.Spider):
    name = "newcar"
    custom_settings = {"FEEDS": {"data/cars.csv": {"format": "csv"}}}

    def start_requests(self):
        yield scrapy.Request(
            url="https://vehiculos.tucarro.com.co/carro_ITEM*CONDITION_2230284_NoIndex_True",
            callback=self.parse,
            meta={"offset": 1},
        )

    def parse(self, response):
        offset = response.meta["offset"]

        cars = response.xpath("//li[@class='ui-search-layout__item']")
        for car in cars:
            yield {
                "name": car.xpath(
                    ".//h2[@class='ui-search-item__title shops__item-title']/text()"
                ).get(),
                "generation": car.xpath(
                    ".//li[@class='ui-search-card-attributes__attribute'][1]/text()"
                ).get(),
                "price": car.xpath(
                    ".//span[@class='price-tag-text-sr-only']/text()"
                ).get(),
                "ubication": car.xpath(
                    ".//span[@class='ui-search-item__group__element ui-search-item__location shops__items-group-details']/text()"
                ).get(),
            }
        
        next = response.xpath("//a[@title='Siguiente']")
        if next:
            yield scrapy.Request(
            url=f"https://vehiculos.tucarro.com.co/carro_Desde_{offset + 48}_ITEM*CONDITION_2230284_NoIndex_True",
            callback=self.parse,
            meta={"offset": offset + 48},
        )
