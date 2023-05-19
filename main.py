from tucarro.tucarro.spiders.newmotor import NewmotorSpider
from tucarro.tucarro.spiders.newcar import NewcarSpider
from scrapy.utils.project import get_project_settings
from scrapy.utils.log import configure_logging
from scrapy.crawler import CrawlerRunner
from twisted.internet import reactor
import pandas as pd


def extract_data():
    configure_logging()

    settings = get_project_settings()
    runner = CrawlerRunner(settings)
    runner.crawl(NewcarSpider)
    runner.crawl(NewmotorSpider)
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())

    reactor.run() 
    return True


def clean_data():
    cars = pd.read_csv("tucarro/data/cars.csv")
    motors = pd.read_csv("tucarro/data/motor.csv")

    cars["price"] = cars.price.str.replace(" pesos", "")
    cars[["city", "departament"]] = cars.ubication.str.split("-", expand=True)
    cars.drop(["ubication"], axis=1, inplace=True)
    cars["price"] = cars["price"].astype("float64")
    cars["generation"] = cars["generation"].astype("int")

    motors["price"] = motors.price.str.replace(" pesos", "")
    motors[["city", "departament"]] = motors.ubication.str.split("-", expand=True)
    motors.drop(["ubication"], axis=1, inplace=True)
    motors["price"] = motors["price"].astype("float64")
    motors["generation"] = motors["generation"].astype("int")

    cars.to_csv("clean_data/new_cars.csv", index=False)
    motors.to_csv("clean_data/new_motors.csv", index=False)


if __name__ == "__main__":
    extract_data()
    if extract_data():
        clean_data()
        print("process completed successfully")
