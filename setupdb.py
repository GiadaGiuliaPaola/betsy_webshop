import models  # Import your models module
from peewee import SqliteDatabase
from models import *

def main():
    setup_data()

def setup_data():
    """
    Creates the database and fills it with data.
    """
   
    product_data = [
        {
            'name': 'Jeans',
            'description': 'durable denim',
            'price': 68.50,
            'quantity_instock': 15,
            'tag': 'pants'
        },
        {
            'name': 'silk shirt',
            'description': 'hypoallergenic silk',
            'price': 30.50,
            'quantity_instock': 25,
            'tag': 'top'
        },
        {
            'name': 'pile sweater',
            'description': 'warm and cozy',
            'price': 25.30,
            'quantity_instock': 18,
            'tag': 'sweater'
        },
        {
            'name': 'cotton sweater',
            'description': 'vegan sweater',
            'price': 15.50,
            'quantity_instock': 12,
            'tag': 'sweater'
        }
    ]

    user_data = [
    (
        "Martijn",
        "Martinusstraat 57",
        "1097BA",
        "Martijn Wonderwerf",
        "visa",
        [
            ("Jeans", 68.50, 2),
            ("silk shirt", 30.50, 3),
            ("pile sweater", 25.30, 1),
        ],
    ),
    (
        "Elisabetta",
        "Caorleweg 12",
        "3021CG",
        "Elisabetta Cats",
        "mastercard",
        [
            ("pile sweater", 25.30, 2),
            ("cotton sweater", 15.50, 1),
        ],
    ),
    (
        "Charlotte",
        "Mijdrechtplein 57",
        "1039HA",
        "Charlotte Mum",
        "american express",
        [
            ("Jeans", 68.50, 1),
            ("pile sweater", 25.30, 3),
            ("cotton sweater", 15.50, 2),
        ],
    )
]


    transaction_data = [
        {
            'product_id': 3,
            'sold_date': '10-10-2023',
            'user_id': 1,
            'quantity_purchased': 2
        },
        {
            'product_id': 2,
            'sold_date': '29-09-2023',
            'user_id': 2,
            'quantity_purchased': 3
        },
        {
            'product_id': 1,
            'sold_date': '12-09-2023',
            'user_id': 3,
            'quantity_purchased': 1
        }
    ]

    initial_tags = ["sweater", "pants", "jacket", "top", "accessories"]

    db = SqliteDatabase("betsy_database.db")
    
    models.db.connect()
    models.db.create_tables(
        [
            models.User,
            models.Product,
            models.Transaction,
            models.ProductsOwnedBy,
            models.Tag
        ], safe=True)
    
    # Insert data into the tables
    with db.atomic():
        models.Tag.insert_many([{"tag": tag} for tag in initial_tags]).execute()
        # Insert product_data
        for product_info in product_data:
            product = models.Product.create(**product_info)

        # Insert user_data
        for user_info in user_data:
            user = models.User.create(
                name=user_info[0],
                address=user_info[1],
                postal_code=user_info[2],
                card_holder=user_info[3],
                payment_method=user_info[4]
            )
            for product_owned_info in user_info[5]:
                product = models.Product.get(models.Product.name == product_owned_info[0])
                quantity = product_owned_info[2]
                models.ProductsOwnedBy.create(user=user, product=product, quantity=quantity)

        # Insert transaction_data
        for transaction_info in transaction_data:
            models.Transaction.create(**transaction_info)

    db.close()


if __name__ == "__main__":
    main()
    