import pytest
import os
from src.database.db_manager import DatabaseManager
from src.logic.billing import BillingLogic

@pytest.fixture
def db():
    db_path = "test_pytest.db"
    if os.path.exists(db_path): os.remove(db_path)
    db_mgr = DatabaseManager(db_path)
    yield db_mgr
    if os.path.exists(db_path): os.remove(db_path)

def test_user_auth(db):
    assert db.authenticate_user("admin", "admin123") is not None
    assert db.add_user("test", "test123", "Staff") is True
    assert db.authenticate_user("test", "test123")['username'] == "test"

def test_menu_crud(db):
    db.add_category("Drinks")
    cats = db.get_categories()
    assert len(cats) == 1
    db.add_menu_item(cats[0]['id'], "Water", 1.0)
    items = db.get_menu_items()
    assert len(items) == 1
    assert items[0]['name'] == "Water"

def test_billing_logic():
    items = [{'price': 100, 'quantity': 2}]
    res = BillingLogic.calculate_totals(items, 10, 5)
    # subtotal = 200
    # discount = 10 (5% of 200)
    # taxable = 190
    # tax = 19 (10% of 190)
    # total = 209
    assert res['total'] == 209.0

def test_tables(db):
    db.add_table("T1", 4)
    tables = db.get_tables()
    assert len(tables) == 1
    assert tables[0]['status'] == 'Available'

    oid = db.create_order(tables[0]['id'], "Dine-in")
    assert db.get_tables()[0]['status'] == 'Occupied'

    db.update_order_payment(oid, 10, 1, 0, 11, "Cash")
    assert db.get_tables()[0]['status'] == 'Available'
