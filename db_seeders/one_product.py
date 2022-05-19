import pendulum

import sys

sys.path.append('../pwp')
import models
from database import SessionLocal

db = SessionLocal()

price = 13.10
name = "Jose Premium Red Orange Flavoured Gin 70cl"

db_product = models.Product(name=name, current_price=price, current_quantity=71)

db_brand = db.query(models.Brand).filter(models.Brand.name == "Jose").first()
db_category = db.query(models.ProductCategory).filter(models.ProductCategory.name == "Spirits & liqueurs").first()

db_product.brand = db_brand
db_product.category = db_category

price_changes = list()

cur_price = price

for i in range(44):
    if i == 7:
        cur_price = round(cur_price * 0.9, 2)
    elif i == 10:
        cur_price = round(cur_price * 0.95, 2)
    elif i == 20:
        cur_price = round(cur_price * 0.91, 2)
    elif i == 29:
        cur_price = round(cur_price * 0.93, 2)
    elif i == 38:
        cur_price = round(cur_price * 1.1, 2)

    price_changes.append(models.PriceChange(price=cur_price,
                                            datetime_of_change=pendulum.datetime(2022, 6, 6).subtract(days=i)))
    # print(pendulum.datetime(2022, 6, 6).subtract(days=i), " price: ", cur_price)


db_product.price_changes = price_changes

sales = list()

# Na początku jest 22

sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 4, 24), product=db_product, sale_quantity=1, sale_price=10.43))
# Przyszło 40 sztuk, jest 61
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 4, 26), product=db_product, sale_quantity=2, sale_price=10.43))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 4, 27), product=db_product, sale_quantity=1, sale_price=10.43))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 4, 29), product=db_product, sale_quantity=3, sale_price=10.43))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 4, 30), product=db_product, sale_quantity=3, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 1), product=db_product, sale_quantity=4, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 2), product=db_product, sale_quantity=6, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 3), product=db_product, sale_quantity=6, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 4), product=db_product, sale_quantity=7, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 5), product=db_product, sale_quantity=8, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 6), product=db_product, sale_quantity=12, sale_price=9.48))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 7), product=db_product, sale_quantity=9, sale_price=9.48))
# Tu brakło towaru 2022, 5, 8
# Przyszło 40, jest 40
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 9), product=db_product, sale_quantity=10, sale_price=10.19))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 10), product=db_product, sale_quantity=11, sale_price=10.19))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 11), product=db_product, sale_quantity=6, sale_price=10.19))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 12), product=db_product, sale_quantity=7, sale_price=10.19))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 13), product=db_product, sale_quantity=9, sale_price=10.19))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 14), product=db_product, sale_quantity=4, sale_price=10.19))
# Brakło towaru
# Przyszło 70, jest 70
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 17), product=db_product, sale_quantity=18, sale_price=10.19))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 18), product=db_product, sale_quantity=15, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 19), product=db_product, sale_quantity=11, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 20), product=db_product, sale_quantity=16, sale_price=11.2))
# Zostało 10
# Przyszło 80, jest 90
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 21), product=db_product, sale_quantity=20, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 22), product=db_product, sale_quantity=18, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 23), product=db_product, sale_quantity=19, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 24), product=db_product, sale_quantity=21, sale_price=11.2))
# Zostało 12
# Przyszło 100, jest 112
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 25), product=db_product, sale_quantity=22, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 26), product=db_product, sale_quantity=23, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 27), product=db_product, sale_quantity=25, sale_price=11.2))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 28), product=db_product, sale_quantity=24, sale_price=11.79))
# Zostało 18
# Przyszło 100, jest 118
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 29), product=db_product, sale_quantity=26, sale_price=11.79))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 30), product=db_product, sale_quantity=23, sale_price=11.79))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 5, 31), product=db_product, sale_quantity=19, sale_price=13.1))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 6, 1), product=db_product, sale_quantity=19, sale_price=13.1))
# Zostało 31
# Przyszło 120, jest 151
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 6, 2), product=db_product, sale_quantity=17, sale_price=13.1))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 6, 3), product=db_product, sale_quantity=15, sale_price=13.1))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 6, 4), product=db_product, sale_quantity=16, sale_price=13.1))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 6, 5), product=db_product, sale_quantity=18, sale_price=13.1))
sales.append(models.Sale(datetime_of_sale=pendulum.datetime(2022, 6, 6), product=db_product, sale_quantity=14, sale_price=13.1))
# Jest 71


db_product.sales = sales


deliveries = list()

deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 4, 26),product=db_product, quantity=40, unit_price=7.20))
deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 5, 9),product=db_product, quantity=40, unit_price=7.50))
deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 5, 17),product=db_product, quantity=70, unit_price=7.50))
deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 5, 21),product=db_product, quantity=80, unit_price=7.40))
deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 5, 25),product=db_product, quantity=100, unit_price=7.35))
deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 5, 29),product=db_product, quantity=100, unit_price=7.35))
deliveries.append(models.Delivery(datetime_of_delivery=pendulum.datetime(2022, 6, 2),product=db_product, quantity=120, unit_price=7.40))

db_product.sales = sales


db.add(db_product)
db.commit()
