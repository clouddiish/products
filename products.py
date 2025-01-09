from pymongo import MongoClient
from credentials import connection_string


class WrongNameError(Exception):
    pass


def get_empty_collection(connection_url, db_name, collection_name):
    client = MongoClient(connection_url)

    # get the database, create database if it doesn't exists
    db = client[db_name]

    # if the collection already exists, drop it
    collections_list = db.list_collection_names()
    if collection_name in collections_list:
        db[collection_name].drop()

    # create and get new collection
    collection = db[collection_name]

    return collection


def init_collection(collection):

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

    collection.insert_many(initial_data)


def get_product_data():
    try:
        name = input("Name of the product: ")
        category = input("Category of the product: ")
        price = float(input("Price of the product: "))

        if not name:
            raise WrongNameError

        return name, category, price

    except ValueError:
        print("Price must be a number. Try again.")

    except WrongNameError:
        print("Name cannot be empty. Try again.")


def add_product(collection):
    data = get_product_data()

    if data:
        name, category, price = data

        new_product = {"name": name, "category": category, "price": price}

        added = collection.insert_one(new_product)

        print(f"Product with id {added.inserted_id} was added.")


def delete_product(collection):
    delete_name = input("Name of the product to delete: ")

    to_delete = {"name": delete_name}

    deleted = collection.delete_many(to_delete)

    print(f"Deleted {deleted.deleted_count} documents.")


def update_product(collection):
    update_name = input("Name of the product to update: ")

    to_update = {"name": update_name}

    data = get_product_data()

    if data:
        name, category, price = data

        new_values = {"name": name, "category": category, "price": price}

        updated = collection.update_one(to_update, {"$set": new_values})

        print(f"Updated {updated.modified_count} documents.")


def run():
    products = get_empty_collection(connection_string, "shop", "products")
    init_collection(products)
    add_product(products)
    # delete_product(products)
    update_product(products)


run()
