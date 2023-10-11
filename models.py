# Models go here
import peewee


db = peewee.SqliteDatabase("betsy_database.db")

class User(peewee.Model):
    name = peewee.CharField()
    address = peewee.CharField()
    postal_code = peewee.CharField()
    card_holder = peewee.CharField()
    payment_method = peewee.CharField()

    class Meta:
        database = db

class Tag(peewee.Model):
    tag = peewee.CharField(unique=True)

    class Meta:
        database = db

class Product(peewee.Model):
    name = peewee.CharField()
    description = peewee.CharField(null=True)
    price = peewee.DecimalField(max_digits=10, decimal_places=2)
    quantity_instock = peewee.IntegerField(constraints=[peewee.Check("quantity_instock >= 0")])
    tag = peewee.CharField()

    class Meta:
        database = db

class Transaction(peewee.Model):
    product_id = peewee.ForeignKeyField(Product)
    sold_date = peewee.DateField()
    user_id = peewee.ForeignKeyField(User)
    quantity_purchased = peewee.IntegerField(constraints=[peewee.Check("quantity_purchased >= 0")])

    class Meta:
        database = db

class ProductsOwnedBy(peewee.Model):
    user = peewee.ForeignKeyField(User)
    product = peewee.ForeignKeyField(Product)

    class Meta:
        database = db

# Define the Many-to-Many relationship between User and Product through ProductsOwnedBy
User.products = peewee.ManyToManyField(Product, backref='users')
