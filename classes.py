from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship

from app import app


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column()
    last_name = Column()
    age = Column()
    email = Column()
    role = Column()
    phone = Column()


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    name = Column()
    description = Column()
    start_date = Column()
    end_date = Column()
    adress = Column()
    price = Column()
    customer_id = Column()
    executor_id = Column()


class Offer(db.Model):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True)
    order_id = Column()
    executor_id = Column()




