"""CRUD operations for the ecommerce database models."""

from db_config import session_scope
from models import User, Product, Order, OrderItem
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select

# User CRUD
def add_user(name, email):
    """Add a new user with a unique email."""
    try:
        with session_scope() as session:
            new_user = User(name=name, email=email)
            session.add(new_user)
            return f'User {name!r} added.'
    except IntegrityError:
        return f'User with email {email!r} already exists.'

def get_user(user_id):
    """Retrieve a user by ID."""
    with session_scope() as session:
        user = session.get(User, user_id)
        return user.to_dict() if user else None

def get_all_users():
    """Retrieve all users as a list of dictionaries."""
    with session_scope() as session:
        users = session.execute(select(User)).scalars().all()
        return [user.to_dict() for user in users]

def update_user(user_id, name=None, email=None):
    """Update a user's name and/or email."""
    with session_scope() as session:
        user = session.get(User, user_id)
        if user:
            if name:
                user.name = name
            if email:
                user.email = email
            return f'User {user_id} updated.'
        return f'User {user_id} not found.'

def delete_user(user_id):
    """Delete a user by ID."""
    with session_scope() as session:
        user = session.get(User, user_id)
        if user:
            session.delete(user)
            return f'User {user_id} deleted.'
        return f'User {user_id} not found.'

# Product CRUD
def add_product(name, price):
    """Add a new product with a name and price."""
    with session_scope() as session:
        new_product = Product(name=name, price=price)
        session.add(new_product)
        return f'Product {name!r} added.'

def get_product(product_id):
    """Retrieve a product by ID."""
    with session_scope() as session:
        product = session.get(Product, product_id)
        return product.to_dict() if product else None

def get_all_products():
    """Retrieve all products as a list of dictionaries."""
    with session_scope() as session:
        products = session.execute(select(Product)).scalars().all()
        return [product.to_dict() for product in products]

def delete_product(product_id):
    """Delete a product by ID."""
    with session_scope() as session:
        product = session.get(Product, product_id)
        if product:
            session.delete(product)
            return f'Product {product_id} deleted.'
        return f'Product {product_id} not found.'

# Order CRUD
def add_order(user_id):
    """Create a new order for a given user ID."""
    with session_scope() as session:
        new_order = Order(user_id=user_id)
        session.add(new_order)
        session.flush()  # Assigns new_order.id
        return new_order.id  # ✅ just the integer ID

def add_order_item(order_id, product_id, quantity):
    """Add an item to an order with specified quantity."""
    with session_scope() as session:
        new_item = OrderItem(order_id=order_id, product_id=product_id, quantity=quantity)
        session.add(new_item)
        return f'Added product {product_id} to order {order_id}.'
