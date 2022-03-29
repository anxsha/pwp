import random

import models
from werkzeug.security import check_password_hash, generate_password_hash
from database import SessionLocal
import pendulum
db = SessionLocal()

# username = "admin"
# password = "admin"
# first_name = "admin"
# last_name = "admin"
# position = models.Position.coordinator
# hashed_password = generate_password_hash(password)
# db_user = models.User(username=username, password=hashed_password, first_name=first_name,
#                       last_name=last_name, position=position)
# db.add(db_user)
# db.commit()


db_brand1 = models.Brand(name="Coca Cola")

db_category1 = models.ProductCategory(name="Napoje")

db_product1 = models.Product(name="Cola zero", current_price=8.10, current_quantity=50)
db_product1.brand = db_brand1
db_product1.category = db.query(models.ProductCategory).filter(models.ProductCategory.name == "Napoje").first()


price_changes = list()

for i in range(10):
    price_changes.append(models.PriceChange(price=round(random.uniform(7.50, 9.99), 2), datetime_of_change=pendulum.now().subtract(days=i)))

db_product1.price_changes = price_changes

db.add(db_product1)
db.commit()
