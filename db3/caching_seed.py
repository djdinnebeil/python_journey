from crud import add_user, add_order, add_order_item, add_product
import random

from db_config import db

db.set_session(database_url='sqlite:///caching_test.db')

# Create products
for i in range(1, 11):
    add_product(f'Product {i}', price=i * 10)

# Create users and orders
for uid in range(1, 6):
    add_user(f'User {uid}', f'user{uid}@email.com')
    oid = add_order(uid)
    for pid in range(1, 6):
        add_order_item(order_id=oid, product_id=pid, quantity=random.randint(1, 5))
