from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from db_config import db
from sqlalchemy import Index

Base = db.Base

class User(Base):
    """Represents a user who can place orders."""
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    email = Column(String, unique=True)
    orders = relationship('Order', back_populates='user')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'email': self.email}

    def __str__(self):
        return f'User(id={self.id}, name={self.name!r}, email={self.email!r})'

    __repr__ = __str__

class Product(Base):
    """Represents a product that can be added to an order."""
    __tablename__ = 'products'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    price = Column(Integer)
    order_items = relationship('OrderItem', back_populates='product')

    def to_dict(self):
        return {'id': self.id, 'name': self.name, 'price': self.price}

    def __str__(self):
        return f'Product(id={self.id}, name={self.name!r}, price={self.price})'

    __repr__ = __str__

class Order(Base):
    """Represents a customer's order. Each order is placed by one user and can contain many items."""
    __tablename__ = 'orders'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), index=True)
    user = relationship('User', back_populates='orders')
    order_items = relationship('OrderItem', back_populates='order')

    def to_dict(self):
        return {'id': self.id, 'user_id': self.user_id}

    def __str__(self):
        return f'Order(id={self.id}, user_id={self.user_id})'

    __repr__ = __str__

class OrderItem(Base):
    """Represents a line item within an order, linking a product to an order."""
    __tablename__ = 'order_items'
    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey('orders.id'), index=True)
    product_id = Column(Integer, ForeignKey('products.id'), index=True)
    quantity = Column(Integer)

    order = relationship('Order', back_populates='order_items')
    product = relationship('Product', back_populates='order_items')

    def to_dict(self):
        return {
            'id': self.id,
            'order_id': self.order_id,
            'product_id': self.product_id,
            'quantity': self.quantity
        }

    def __str__(self):
        return (
            f'OrderItem(id={self.id}, order_id={self.order_id}, '
            f'product_id={self.product_id}, quantity={self.quantity})'
        )

    __repr__ = __str__
