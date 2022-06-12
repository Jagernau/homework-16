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
