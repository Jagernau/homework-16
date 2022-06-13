from flask import Flask, jsonify, request

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, ForeignKey, Date, Text, Float
from json import loads

import funcions
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///test.db"
app.config['JSON_SORT_KEYS'] = False
app.config['JSON_AS_ASCII'] = False

db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String(100))
    last_name = Column(String(100))
    age = Column(Integer)
    email = Column(String(50))
    role = Column(String(50))
    phone = Column(String(50))


class Order(db.Model):
    __tablename__ = "order"
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    description = Column(Text)
    start_date = Column(Date)
    end_date = Column(Date)
    address = Column(String(150))
    price = Column(Float)
    customer_id = Column(Integer, ForeignKey("user.id"))
    executor_id = Column(Integer, ForeignKey("user.id"))
    #users = relationship("User")
#customer_id - id создателя, от user_id
#executor_id - id исполнителя, от user_id


class Offer(db.Model):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("user.id"))
    executor_id = Column(Integer, ForeignKey("user.id"))
    #orders = relationship("Order")
    #users  = relationship("User")
#executor_id - зависит от usr_id
#order_id- зависит от order_id

db.drop_all()
db.create_all()



for i in funcions.get_js_users():
    db.session.add(User(
        id=i["id"], 
        first_name=i["first_name"], 
        last_name=i["last_name"], 
        age=i["age"], 
        email=i["email"], 
        role=i["role"], 
        phone=i["phone"]
    ))


for i in funcions.get_js_orders():
    month_start, day_start, year_start = i["start_date"].split("/")
    month_end, day_end, year_end = i["end_date"].split("/")

    db.session.add(Order(
        id=i["id"], 
        name=i["name"], 
        description=i["description"], 
        start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
        end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
        address=i["address"], 
        price=i["price"], 
        customer_id=i["customer_id"], 
        executor_id=i["executor_id"]
    ))


for i in funcions.get_js_offers():
    db.session.add(Offer(
        id=i["id"],
        order_id=i["order_id"],
        executor_id=i["executor_id"]
    ))

db.session.commit()




@app.route("/users", methods=['GET', 'POST'])
def get_all_users():
    if request.method == 'GET':
        all_users = User.query.all()
        return jsonify(funcions.user_query(all_users))

    if request.method == 'POST':
        user = loads(request.data)
        new_user_obj = User(
            id=user['id'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            age=user['age'],
            email=user['email'],
            role=user['role'],
            phone=user['phone'])
        db.session.add(new_user_obj)
        db.session.commit()
        db.session.close()
        return "Пользователь добавлен", 200






@app.route("/users/<sid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_user(sid):
    if request.method == 'GET':
        one_user = db.session.query(User).filter(User.id==sid).all()
        return jsonify(funcions.user_query(one_user))
    if request.method == 'PUT':
        user_data = loads(request.data)
        user = db.session.query(User).get(sid)

        user.first_name = user_data['first_name']
        user.last_name = user_data['last_name']
        user.phone = user_data['phone']
        user.role = user_data['role']
        user.email = user_data['email']
        user.age = user_data['age']
        db.session.add(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {sid} изменён", 200

    if request.method == 'DELETE':
        user = db.session.query(User).get(sid)
        db.session.delete(user)
        db.session.commit()
        db.session.close()
        return f"Пользователь с id {sid} удалён", 200



@app.route("/orders", methods=['GET', 'POST'])
def get_all_orders():
    if request.method == 'GET':
        all_orders = Order.query.all()
        return jsonify(funcions.order_query(all_orders))
    if request.method == 'POST':
        order = loads(request.data)
        month_start, day_start, year_start = order["start_date"].split("/")
        month_end, day_end, year_end = order["end_date"].split("/")
        new_order_obj = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start)),
            end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end)),
            adress=order['address'],
            price=order['price'],
            customer_id=order['customer_id'],
            executor_id=order['executor_id'])
        db.session.add(new_order_obj)
        db.session.commit()
        db.session.close()
        return "Заказ создан", 200
            




@app.route("/orders/<sid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_order(sid):
    if request.method == 'GET':
        one_order = db.session.query(Order).filter(Order.id==sid)
        return jsonify(funcions.order_query(one_order))
    if request.method == 'PUT':
        order_data = loads(request.data)
        order = db.session.query(Order).get(sid)

        month_start, day_start, year_start = order_data["start_date"].split("/")
        month_end, day_end, year_end = order_data["end_date"].split("/")

        order.name=order_data['name']
        order.description=order_data['description']
        order.start_date=datetime.date(year=int(year_start), month=int(month_start), day=int(day_start))
        order.end_date=datetime.date(year=int(year_end), month=int(month_end), day=int(day_end))
        order.adress=order_data['address']
        order.price=order_data['price']
        order.customer_id=order_data['customer_id']
        order.executor_id=order_data['executor_id']

        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ {sid} изменён"

    if request.method == 'DELETE':
        order = db.session.query(Order).get(sid)
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ {sid} удалён"







@app.route("/offers", methods=['GET','POST'])
def get_all_offers():
    if request.method == 'GET':
        all_offers = Offer.query.all()
        return jsonify(funcions.offer_query(all_offers))
    if request.method == 'POST':
        offer = loads(request.data)
        new_offer_obj = Offer(
            id=offer["id"],
            order_id=offer['order_id'],
            executor_id=offer['executor_id']
        )
        db.session.add(new_offer_obj)
        db.session.commit()
        db.session.close()
        return "Предложение создано", 200



if __name__ == '__main__':
    app.run()


