import pytest
from app import app, db
from models import Product, Location, ProductMovement
from sqlalchemy import text


@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()


def test_balance_report_basic(client):
    # Create products and locations
    p1 = Product(product_id='P1', name='Prod1')
    p2 = Product(product_id='P2', name='Prod2')
    l1 = Location(location_id='L1', name='Loc1')
    l2 = Location(location_id='L2', name='Loc2')
    db.session.add_all([p1, p2, l1, l2])
    db.session.commit()

    # Movements:
    # P1: +10 to L1, -3 from L1, +5 to L2
    db.session.add(ProductMovement(from_location=None, to_location='L1', product_id='P1', qty=10))
    db.session.add(ProductMovement(from_location='L1', to_location=None, product_id='P1', qty=3))
    db.session.add(ProductMovement(from_location=None, to_location='L2', product_id='P1', qty=5))

    # P2: +7 to L2
    db.session.add(ProductMovement(from_location=None, to_location='L2', product_id='P2', qty=7))

    db.session.commit()

    sql = """
    SELECT p.product_id, l.location_id,
           COALESCE(
             SUM(CASE WHEN pm.to_location = l.location_id THEN pm.qty ELSE 0 END) -
             SUM(CASE WHEN pm.from_location = l.location_id THEN pm.qty ELSE 0 END), 0
           ) AS balance
    FROM product p
    CROSS JOIN location l
    LEFT JOIN product_movement pm
      ON pm.product_id = p.product_id
      AND (pm.to_location = l.location_id OR pm.from_location = l.location_id)
    GROUP BY p.product_id, l.location_id
    ORDER BY p.product_id, l.location_id;
    """

    result = db.session.execute(text(sql)).fetchall()
    # Build dict {(product,location): balance}
    balances = {(r[0], r[1]): r[2] for r in result}

    assert balances[('P1', 'L1')] == 7  # 10 in - 3 out
    assert balances[('P1', 'L2')] == 5
    assert balances[('P2', 'L2')] == 7
    assert balances[('P2', 'L1')] == 0
