# main.py
from crud import add_user, get_user, add_product, get_product, add_order, add_order_item, get_all_products, delete_user
from crud import get_all_users
# from db_config import Base, engine
from sqlalchemy.orm import sessionmaker

from crud import delete_user
from db_config import set_session

set_session(database_url='sqlite:///e2.db')

add_user('DJ', 'djdinn')
add_user('Daniel', 'ddinn')
# Get and display users
print(get_user(1))
print(get_user(2))

# Add products
add_product("Laptop", 1200)
add_product("Phone", 700)

# Get and display products
print(get_product(1))
print(get_product(2))

# Create an order and add items to that order (dynamically)
order_id = add_order(1)
add_order_item(order_id, 1, 2)  # 2 Laptops
add_order_item(order_id, 2, 1)  # 1 Phone

print(get_all_users())

print(get_all_products())

print(delete_user(1))
print(get_all_users())