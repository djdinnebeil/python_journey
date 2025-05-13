import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Product, Order, OrderItem
from crud import get_all_users, add_user
from db_config import set_session

@pytest.fixture(scope="function")
def test_session():
    # Set up in-memory DB and session factory
    Session = set_session(database_url='sqlite:///:memory:')
    session = Session()
    yield session
    session.close()

def test_user_crud(test_session):
    with test_session.begin():
        user = User(name="Alice", email="alice@example.com")
        test_session.add(user)

    with test_session.begin():
        result = test_session.query(User).filter_by(name="Alice").first()
        assert result.email == "alice@example.com"

def test_product_crud(test_session):
    with test_session.begin():
        product = Product(name="Laptop", price=1500)
        test_session.add(product)

    with test_session.begin():
        result = test_session.query(Product).filter_by(name="Laptop").first()
        assert result.price == 1500

def test_order_crud(test_session):
    with test_session.begin():
        user = User(name="Bob", email="bob@example.com")
        product = Product(name="Phone", price=800)
        test_session.add_all([user, product])

    with test_session.begin():
        user = test_session.query(User).filter_by(name="Bob").first()
        order = Order(user_id=user.id)
        test_session.add(order)

    with test_session.begin():
        order = test_session.query(Order).first()
        product = test_session.query(Product).filter_by(name="Phone").first()
        item = OrderItem(order_id=order.id, product_id=product.id, quantity=2)
        test_session.add(item)

    with test_session.begin():
        items = test_session.query(OrderItem).all()
        assert len(items) == 1
        assert items[0].quantity == 2

def test_get_all_users(test_session):
    with test_session.begin():
        add_user('DJ', 'djdinn24')
        add_user('Daniel', 'ddinn24')
        users = get_all_users()
        assert 'DJ' in users[0]['name']
        assert 'Daniel' in users[1]['name']
