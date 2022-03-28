import models
from werkzeug.security import check_password_hash, generate_password_hash
from database import SessionLocal

db = SessionLocal()

username = "admin"
password = "admin"
first_name = "admin"
last_name = "admin"
position = models.Position.coordinator
hashed_password = generate_password_hash(password)
db_user = models.User(username=username, password=hashed_password, first_name=first_name,
                      last_name=last_name, position=position)
db.add(db_user)
db.commit()
