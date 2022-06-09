from flask import Flask
import utils
import classes


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"


@app.route("/users")
def get_all_users():




@app.route("/users/<id>")
def get_one_user(id):





@app.route("/orders")
def get_all_orders():




@app.route("/orders/<id>")
def get_one_order(id):





@app.route("/offers")
def get_all_offers():





@app.route("/offers/<id>")
def get_one_offer(id):





