from flask import Flask, jsonify, request
from sqlalchemy.orm import relationship
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Column, Integer, ForeignKey, Date, Text, Float
from json import loads

import funcions
import datetime

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"
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
    customer = relationship("User", foreign_keys=[customer_id])
    executor = relationship("User", foreign_keys=[executor_id])


#customer_id - id создателя, от user_id
#executor_id - id исполнителя, от user_id


class Offer(db.Model):
    __tablename__ = "offer"
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    executor_id = Column(Integer, ForeignKey("user.id"))
    order = relationship("Order", foreign_keys=[order_id])
    executor = relationship("User", foreign_keys=[executor_id])


#executor_id - зависит от usr_id
#order_id- зависит от order_id


db.create_all()


for i in funcions.get_files_users():
    db.session.add(User(
        id=i["id"], 
        first_name=i["first_name"], 
        last_name=i["last_name"], 
        age=i["age"], 
        email=i["email"], 
        role=i["role"], 
        phone=i["phone"]
    ))


for i in funcions.get_files_orders():
    db.session.add(Order(
        id=i["id"], 
        name=i["name"], 
        description=i["description"], 
        start_date=datetime.datetime.strptime(i["start_date"], '%m/%d/%Y'),
        end_date=datetime.datetime.strptime(i["end_date"], '%m/%d/%Y'),
        address=i["address"], 
        price=i["price"], 
        customer_id=i["customer_id"], 
        executor_id=i["executor_id"]
    ))


for i in funcions.get_files_offers():
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
        new_order_obj = Order(
            id=order['id'],
            name=order['name'],
            description=order['description'],
            start_date=datetime.datetime.strptime(order["start_date"], '%m/%d/%Y'),
            end_date=datetime.datetime.strptime(order["end_date"], '%m/%d/%Y'),
            address=order['address'],
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


        order.name=order_data['name']
        order.description=order_data['description']
        order.start_date=datetime.datetime.strptime(order_data["start_date"], '%m/%d/%Y')
        order.end_date=datetime.datetime.strptime(order_data["end_date"], '%m/%d/%Y')
        order.address=order_data['address']
        order.price=order_data['price']
        order.customer_id=order_data['customer_id']
        order.executor_id=order_data['executor_id']

        db.session.add(order)
        db.session.commit()
        db.session.close()
        return f"Заказ {sid} изменён", 200

    if request.method == 'DELETE':
        order = db.session.query(Order).get(sid)
        db.session.delete(order)
        db.session.commit()
        db.session.close()
        return f"Заказ {sid} удалён", 200




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



@app.route("/offers/<sid>", methods=['GET', 'PUT', 'DELETE'])
def get_one_offer(sid):
    if request.method == 'GET':
        one_offer = db.session.query(Offer).filter(Offer.id == sid)
        return jsonify(funcions.offer_query(one_offer))
    if request.method == 'PUT':
        offer_data = loads(request.data)
        offer = db.session.query(Offer).get(sid)

        offer.order_id = offer_data['order_id']
        offer.executor_id = offer_data['executor_id']
        db.session.add(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение {sid} изменено", 200

    if request.method == 'DELETE':
        offer = db.session.query(Offer).get(sid)
        db.session.delete(offer)
        db.session.commit()
        db.session.close()
        return f"Предложение {sid} удалено", 200


if __name__ == '__main__':
    app.run()

