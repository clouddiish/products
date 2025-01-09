from pymongo import MongoClient
from credentials import connection_string

client = MongoClient(connection_string)

# get the database, create database if it doesn't exists
shop_db = client["shop"]

# if the collection already exists, drop it
collections_list = shop_db.list_collection_names()
if "products" in collections_list:
    shop_db["products"].drop()

# create and get new collection
products = shop_db["products"]

initial_data = [
    {"name": "sponge", "category": "bathroom", "price": 0.56},
    {"name": "pot", "category": "kitchen", "price": 20.99},
    {"name": "pillow", "category": "bedroom", "price": 5.49},
    {"name": "toothbrush", "category": "bathroom", "price": 2.49},
    {"name": "pan", "category": "kitchen", "price": 15.75},
    {"name": "blanket", "category": "bedroom", "price": 22.00},
    {"name": "soap", "category": "bathroom", "price": 1.25},
    {"name": "knife", "category": "kitchen", "price": 12.89},
    {"name": "lamp", "category": "bedroom", "price": 30.50},
    {"name": "shampoo", "category": "bathroom", "price": 3.99},
    {"name": "spatula", "category": "kitchen", "price": 5.49},
    {"name": "sheet", "category": "bedroom", "price": 14.99},
    {"name": "toilet paper", "category": "bathroom", "price": 0.89},
    {"name": "cutting board", "category": "kitchen", "price": 8.50},
    {"name": "curtains", "category": "bedroom", "price": 45.00},
    {"name": "bath towel", "category": "bathroom", "price": 6.75},
]

products.insert_many(initial_data)
