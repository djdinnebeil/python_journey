import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.future import select
from models import Base, User, Product, Order, OrderItem
from crud import get_all_users, add_user, get_user, add_product, get_product, add_order, add_order_item, delete_user
from db_config import set_session

@pytest.fixture(scope='function')
def test_session():
    """Set up an isolated in-memory database for each test."""
    Session = set_session(database_url='sqlite:///:memory:')
    session = Session()
    yield session
    session.close()


def test_user_crud(test_session):
    user = User(name='Alice', email='alice@example.com')
    test_session.add(user)
    test_session.commit()

    stmt = select(User).filter_by(name='Alice')
    result = test_session.execute(stmt).scalar_one()
    assert result.email == 'alice@example.com'


def test_product_crud(test_session):
    product = Product(name='Laptop', price=1500)
    test_session.add(product)
    test_session.commit()

    stmt = select(Product).filter_by(name='Laptop')
    result = test_session.execute(stmt).scalar_one()
    assert result.price == 1500


def test_order_crud(test_session):
    user = User(name='Bob', email='bob@example.com')
    product = Product(name='Phone', price=800)
    test_session.add_all([user, product])
    test_session.commit()

    order = Order(user_id=user.id)
    test_session.add(order)
    test_session.commit()

    item = OrderItem(order_id=order.id, product_id=product.id, quantity=2)
    test_session.add(item)
    test_session.commit()

    stmt = select(OrderItem).filter_by(order_id=order.id)
    items = test_session.execute(stmt).scalars().all()
    assert len(items) == 1
    assert items[0].quantity == 2


def test_get_all_users(test_session):
    test_session.add_all([
        User(name='DJ', email='djdinn'),
        User(name='Daniel', email='ddinn')
    ])
    test_session.commit()

    users = get_all_users()
    names = [user['name'] for user in users]
    assert 'DJ' in names
    assert 'Daniel' in names


def test_get_user(test_session):
    user = User(name='Charlie', email='charlie@example.com')
    test_session.add(user)
    test_session.commit()

    result = get_user(user.id)
    assert result['name'] == 'Charlie'
    assert result['email'] == 'charlie@example.com'


def test_add_product_and_get_product(test_session):
    msg = add_product('Tablet', 450)
    assert 'added' in msg
    product = get_product(1)
    assert product['name'] == 'Tablet'
    assert product['price'] == 450


def test_add_order_and_items(test_session):
    user = User(name='Eve', email='eve@example.com')
    product = Product(name='Monitor', price=300)
    test_session.add_all([user, product])
    test_session.commit()

    order_id = add_order(user.id)
    msg = add_order_item(order_id, product.id, 1)
    assert str(product.id) in msg
    assert str(order_id) in msg


def test_delete_user(test_session):
    user = User(name='Charlie', email='charlie@example.com')
    test_session.add(user)
    test_session.commit()

    result = delete_user(user.id)
    assert 'User 1 deleted.' == result