from pymongo import MongoClient
from config import MONGO_URI

client = MongoClient(MONGO_URI)
db = client["autobuy"]

orders = db.orders
accounts = db.accounts
plans = db.plans
