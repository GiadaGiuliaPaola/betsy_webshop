﻿# betsy_webshop
Product Management System
This repository contains the Python code for a product management system named "Betsy Webshop." It allows users to search, purchase, manage, and track products with features like:

Fuzzy search: Handles misspelled or uppercase terms in searches.
User product management: List and remove user-owned products.
Tag-based product browsing: View products based on tags, even with slight misspellings or different capitalization.
Inventory control: Add new products, update stock levels, and track purchase transactions.
Code Structure:

models.py: Defines database models using Peewee ORM for products, users, tags, product ownership, and transactions.
setupdb.py: Initializes the database and populates it with sample data (optional).
rapidfuzz.py (external library): Provides fuzzy string matching functionality for search and tag matching.
main.py: Contains the core logic of the application, including functions for:
search(term): Searches for products based on the given term, handling typos and case sensitivity.
list_user_products(user_id): Lists all products owned by a specific user.
list_products_per_tag(tag_id): Lists all products associated with a particular tag, even for misspelled or uppercase tags.
add_product_to_catalog(user_id, product_data): Adds a new product to the catalog and assigns ownership to a user.
update_stock(product_id, new_quantity): Updates the stock quantity for a specific product.
purchase_product(product_id, user_id, quantity, tag_name): Handles a product purchase transaction, updating stock and creating a transaction record.
remove_product(user_id, product_id): Removes a product from a user's ownership.
create_or_get_tag(tag_name): Ensures case-insensitive tag handling by checking for existing tags before creating new ones.
Testing:

The provided code includes commented-out sections for testing various functionalities. You can replace the placeholder values and run the script to test different scenarios.

Disclaimer:

This code is for educational purposes and might require further development for a fully functional web application.
