# MongoDB product manager

MongoDB product manager provides a command-line interface to manage product data in a MongoDB database. It allows users to view, add, update, and delete products, organized by categories.

## features

- view all products in the database
- view products by category with a limit
- add new products
- update existing product details
- delete products by name

## getting started

### dependencies

- Python 3.7 or later
- MongoDB
- Python packages
  - `pymongo`
  - `python-dotenv`
```
pip install pymongo python-dotenv
```

### installation

- clone the repository or download the code files
```
git clone https://github.com/clouddiish/products.git
```
- copy the `.env-example` file to `.env`
- add your MongoDB connection string to the .env file
```
CONNECTION_STRING=mongodb+srv://<username>:<password>@cluster0.mongodb.net/<dbname>?retryWrites=true&w=majority
```

### run 

- run the script with the below command. Note: if needed replace `products.py` with the name of the script
```
python products.py
```

### output 

- on running the program, you'll be presented with a menu of different options:
  - vap - view all products
  - vp - view products by category
  - ap - add product
  - up - update product
  - dp - delete product
  - ex - exit
 
## notes

- the database and collection are recreated every time the application starts, which means all previous data is cleared
- make sure the CONNECTION_STRING in the .env file is correctly set up before running the application.
