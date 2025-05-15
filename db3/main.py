# main.py
from crud_cache import add_user, get_user, get_all_users, add_product, get_product, add_order, add_order_item, get_all_products, delete_user, get_user_orders, get_user_orders_grouped, get_total_quantity_per_product
from utils import view_all_products
from db_config import db

db.set_session(database_url='sqlite:///e2.db')

add_user('DJ', 'djdinn')
add_user('Daniel', 'ddinn')
# Get and display users
print(get_user(1))
print(get_user(2))

# Add products
add_product('Laptop', 1200)
add_product('Phone', 700)

# Get and display products
print(get_product(1))
print(get_product(2))

# Create an order and add items to that order (dynamically)
order_id = add_order(1)
add_order_item(order_id, 1, 2)  # 2 Laptops
add_order_item(order_id, 2, 1)  # 1 Phone

print(get_all_users())

print(get_all_products())

print(get_all_users())

print(get_user_orders(1))

print(get_total_quantity_per_product())

print(get_user_orders_grouped(1))

view_all_products()