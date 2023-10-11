# Do not modify these lines
__winc_id__ = "d7b474e9b3a54d23bca54879a4f1855b"
__human_name__ = "Betsy Webshop"

# Add your code after this line
from models import *
from peewee import *
from datetime import datetime
import os
from setupdb import setup_data
from rapidfuzz import fuzz
import datetime

def main():
    if os.path.exist('betsy_database.db') == False:
        setup_data()

def search(term):
    '''searches the database and returns
    the product name and description, the result will not 
    be affected by spelling mistake or upper case characters'''
    term = term.lower()  # Convert the search term to lowercase
    results = []
    for product in Product.select():
        product_name = product.name.lower()  # Convert product name to lowercase
        product_description = product.description.lower()  # Convert product description to lowercase

        # Use rapidfuzz's fuzz.ratio for comparing the lowercase search term
        if fuzz.ratio(product_name, term) > 70 or fuzz.ratio(product_description, term) > 70:
            results.append(product)
        
    if results:
        return results
    else:
        print(f'Sorry, no {term} found.')
        return []

    
def list_user_products(user_id):
    '''return all the product that belong to a user'''
    products = (Product
            .select()
            .join(ProductsOwnedBy)
            .where(ProductsOwnedBy.user == user_id)
        )
    user_name = User.get(User.id == user_id).name
    product_names = [product.name for product in products]
    
    result = f"{user_name} owned products are: {', '.join(product_names)}"

    return result


def list_products_per_tag(tag_id):
    '''View all products for a given tag, detect the
    tag id even if mispelled or with uppercase'''
    tag_id = tag_id.lower()
    matching_products = set()

    matching_products.update(
        product.name
        for product in Product.select()
        if fuzz.ratio(product.tag.lower(), tag_id) > 70
    )

    similar_tags = [tag for tag in Tag.select() if fuzz.ratio(tag.tag.lower(), tag_id) > 70]

    for tag in similar_tags:
        matching_products.update(
            product.name
            for product in Product.select().where(Product.tag.contains(tag.tag))
        )

    if matching_products:
        return f"With the following tag: {tag_id}, we have items: {', '.join(matching_products)}."
    else:
        return f"No items found in tag {tag_id}."


def add_product_to_catalog(user_id, product_data):
    '''Add a product to a user and in the catalog'''
    user = User.get(User.id == user_id)
    product = Product.create(**product_data)
    ProductsOwnedBy.create(user=user, product=product)
    

def update_stock(product_id, new_quantity):
    '''Update the stock quantity of a product'''
    try:
        product = Product.get(Product.id == product_id)
        product.quantity_instock = new_quantity
        product.save()
        print(f"Updated stock quantity for product ID {product_id} to {new_quantity}.")
    except Product.DoesNotExist:
        print(f"Product with ID {product_id} not found.")


def purchase_product(product_id, user_id, quantity, tag_name):
    '''Handle a purchase between a buyer and a seller for a given product'''
    product = Product.get(Product.id == product_id)
    user = User.get(User.id == user_id)

    tag, created = Tag.get_or_create(tag=tag_name)

    if product.quantity_instock >= quantity:
        transaction_data = {
            'product_id': product_id,
            'sold_date': datetime.date.today(),
            'user_id': user_id,
            'quantity_purchased': quantity,
        }
        product.tag = tag

        print(f"{user.name} purchased {quantity} {product.name}.")
        Transaction.create(**transaction_data)
        product.quantity_instock -= quantity
        product.save()
    else:
        raise ValueError("Insufficient stock for purchase.")


def remove_product(user_id, product_id):
    '''remove a product from a user, first 
    check if the product is owned by the user, then proceed to remove
    the data from the database'''
    user = User.get(User.id == user_id)
    product = Product.get(Product.id == product_id)

    try:
        product = Product.get(Product.id == product_id)
    except Product.DoesNotExist:
        return f"Product with ID {product_id} does not exist."
    
    # Check if the user owns the product
    ownership = ProductsOwnedBy.get((ProductsOwnedBy.user == user) & (ProductsOwnedBy.product == product))
    
    # If the user owns the product, remove it from the user's ownership
    if ownership:
        ownership.delete_instance()
        return f"Removed product with ID {product_id} from user with ID {user_id}."
    else:
        return f"User with ID {user_id} does not own the product with ID {product_id}."


def create_or_get_tag(tag_name):
    tag_name = tag_name.lower()  # Convert the tag name to lowercase for case-insensitive check
    try:
        # Check if a tag with the same name (case-insensitive) already exists
        tag = Tag.get(fn.Lower(Tag.tag)==tag_name)
    except Tag.DoesNotExist:
        # If it doesn't exist, create a new tag
        tag = Tag.create(tag=tag_name)
    return tag

#testing

'''search test'''
# search_results = search("jeins") #write here the name you want to search
# for product in search_results:
#     print(f"Product Name: {product.name}, Description: {product.description}")

'''list_user_products test'''
# user_id = 1  # Replace with the user's ID
# print(list_user_products(user_id))


'''list_products_per_tag test'''
# tag_id = "PAnt"  
# print(list_products_per_tag(tag_id))


'''add_product_to_catalog test'''
# user_id = 3  # Replace with the user's ID
# new_product_data = {
#     'name': 'silk pants',
#     'description': 'total silk',
#     'price': 75.53,
#     'quantity_instock': 15,
#     'tag': 'pants'
# } # replace the data to add a new item
# add_product_to_catalog(user_id, new_product_data)


'''update_stock test'''
# product_id = 3  # Replace with the product's ID
# new_quantity = 50  # Replace with the new quantity
# update_stock(product_id, new_quantity)


'''purchase_product test'''
# product_id = 4  # Replace with the product's ID
# user_id = 2  # Replace with the buyer's ID
# quantity = 1  # Replace with the quantity to purchase
# tag_name = 'sweater'
# purchase_product(product_id, user_id, quantity, tag_name)


'''remove_product test'''
# user_id = 3 # Replace with the user's ID
# product_id = 5  # Replace with the product's ID
# print(remove_product(user_id, product_id))
