from crud import add_user, get_user, get_all_users, add_product, get_product, add_order, add_order_item, get_all_products, delete_user, get_products_paginated
from crud import get_total_quantity_per_product, get_user_orders
from crud import get_user_orders_grouped
from db_config import set_session
from utils import view_all_products

set_session(database_url='sqlite:///e5.db')

print(get_user_orders(1))

print(get_total_quantity_per_product(2))

print(get_user_orders_grouped(1))



print('---')
view_all_products()