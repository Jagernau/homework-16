from json import load


def get_js_users():
    with open("js_files/user.json", "r") as read:
        all_users = load(read)
    return all_users


def get_js_orders():
    with open("js_files/order.json", "r") as read:
        all_orders = load(read)
    return all_orders

def get_js_offers():
    with open("js_files/offer.json", "r") as read:
        all_offers = load(read)
    return all_offers

def user_query(query):
    user_resp = []
    for i in query:
        user_resp.append({"id": i.id, "first_name": i.first_name, "last_name": i.last_name, "age": i.age, "email": i.email, "role": i.role, "phone": i.phone})
    return user_resp

def order_query(query):
    order_resp = []
    for i in query:
        order_resp.append({"id": i.id, "name": i.name, "description": i.description, "start_date": i.start_date, "end_date": i.end_date, "address": i.address, "price": i.price, "customer_id": i.customer_id, "executor_id": i.executor_id })
    return order_resp

def offer_query(query):
    offer_resp = []
    for i in query:
        offer_resp.append({"id": i.id, "order_id": i.order_id, "executor_id": i.executor_id})
    return offer_resp
    
