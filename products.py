import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()
CONNECTION_STRING = os.getenv("CONNECTION_STRING")


class WrongNameError(Exception):
    """Exception raised when the product name is invalid."""

    pass


def get_empty_collection_and_client(connection_url, db_name, collection_name):
    """
    Gets a MongoDB collection, dropping it if it already exists.

    Args:
        connection_url (str): MongoDB connection string.
        db_name (str): Name of the database.
        collection_name (str): Name of the collection.

    Returns:
        tuple: A tuple containing the collection and the MongoDB client.
    """
    client = MongoClient(connection_url)

    # get the database, create database if it doesn't exists
    db = client[db_name]

    # if the collection already exists, drop it
    collections_list = db.list_collection_names()
    if collection_name in collections_list:
        db[collection_name].drop()

    # create and get new collection
    collection = db[collection_name]

    return collection, client


def init_collection(collection):
    """
    Initializes the MongoDB collection with sample product data.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to initialize.
    """
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
    """
    Collects product data from user input.

    Returns:
        tuple: A tuple containing the product name (str), category (str), and price (float),
               or None if invalid input is provided.
    """
    try:
        name = input("Name of the product: ").lower()
        category = input("Category of the product: ").lower()
        price = float(input("Price of the product: "))

        if not name:
            raise WrongNameError

        return name, category, price

    except ValueError:
        print("Price must be a number. Try again.")

    except WrongNameError:
        print("Name cannot be empty. Try again.")


def get_all_products(collection):
    """
    Retrieves and displays all products in the collection.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to query.
    """
    results = collection.find({}, {"_id": 0})

    for row in results:
        print(row)


def get_products_by_category_with_limit(collection):
    """
    Retrieves and displays products from a specific category.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to query.
    """
    try:
        category = input("From which category do you want to see products? ").lower()
        how_many = int(input("How many products do you want to see? "))

        to_find = {"category": category}

        results = collection.find(to_find, {"_id": 0}).limit(how_many)

        for row in results:
            print(row)

    except ValueError:
        print("The number of products to see must be a number. Try again.")


def add_product(collection):
    """
    Adds a new product to the collection.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to modify.
    """
    data = get_product_data()

    if data:
        name, category, price = data

        new_product = {"name": name, "category": category, "price": price}

        added = collection.insert_one(new_product)

        print(f"Product with id {added.inserted_id} was added.")


def delete_product(collection):
    """
    Deletes products from the collection by name.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to modify.
    """
    delete_name = input("Name of the product to delete: ").lower()

    to_delete = {"name": delete_name}

    deleted = collection.delete_many(to_delete)

    print(f"Deleted {deleted.deleted_count} products.")


def update_product(collection):
    """
    Updates the details of a product in the collection.

    Args:
        collection (pymongo.collection.Collection): The MongoDB collection to modify.
    """
    update_name = input("Name of the product to update: ").lower()

    to_update = {"name": update_name}

    data = get_product_data()

    if data:
        name, category, price = data

        new_values = {"name": name, "category": category, "price": price}

        updated = collection.update_one(to_update, {"$set": new_values})

        print(f"Updated {updated.modified_count} products.")


def run():
    """
    Main function to run the application. Initializes the collection and handles user actions.
    """
    products, client = get_empty_collection_and_client(CONNECTION_STRING, "shop", "products")
    init_collection(products)

    while True:
        action = input(
            """
            What do you want to do?
            - vap - view all products
            - vp - view products by category
            - ap - add product
            - up - update product
            - dp - delete product
            - ex - exit
            """
        ).lower()

        match action:
            case "vap":
                get_all_products(products)
            case "vp":
                get_products_by_category_with_limit(products)
                print()
            case "ap":
                add_product(products)
                print()
            case "up":
                update_product(products)
                print()
            case "dp":
                delete_product(products)
                print()
            case "ex":
                sure = input("Are you sure? (Y/N) ").lower()
                if sure == "y":
                    break
            case _:
                print("Invalid option. Try again.")
                print()

    client.close()


run()
