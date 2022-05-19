import csv
import random

import pendulum

import sys


sys.path.append('../pwp')
import models
from database import SessionLocal

db = SessionLocal()

with open('sains_with_brands.csv') as csv_in:
    dr = csv.DictReader(csv_in)
    products = [(i['cat'], i['brand'], i['name'], i['price']) for i in dr]


for product in products:
    category = product[0]
    brand = product[1]
    name = product[2]
    price = float(product[3])

    if not (db_category := db.query(models.ProductCategory).filter(models.ProductCategory.name == category).first()):
        db_category = models.ProductCategory(name=category)

    if not (db_brand := db.query(models.Brand).filter(models.Brand.name == brand).first()):
        db_brand = models.Brand(name=brand)

    db_product = models.Product(name=name, current_price=price, current_quantity=random.randint(2, 40))
    db_product.brand = db_brand
    db_product.category = db_category

    price_changes = list()

    random_distribution = random.randint(0, 1)

    low_price = round(0.9 * price, 2)
    high_price = round(1.1 * price, 2)

    day_interval = random.randint(1, 3)

    for i in range(random.randint(7, 20)):

        if random_distribution == 0:
            price_changes.append(models.PriceChange(price=round(random.uniform(low_price, high_price), 2),
                                                    datetime_of_change=pendulum.now().subtract(days=i * day_interval)))
        elif random_distribution == 1:
            price_changes.append(models.PriceChange(price=round(random.gauss(price, 0.05 * price), 2),
                                                    datetime_of_change=pendulum.now().subtract(days=i * day_interval)))

    db_product.price_changes = price_changes

    db.add(db_product)
    db.commit()


