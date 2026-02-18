import pytest
import os
import sqlite3
from src.database.db_manager import DatabaseManager
from src.logic.billing import BillingLogic

@pytest.fixture
def db():
    db_path = "test_pytest_final.db"
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

def test_foreign_keys(db):
    db.add_category("Test Cat")
    db.add_menu_item(1, "Test Item", 10.0)
    with pytest.raises(sqlite3.IntegrityError):
        with db.get_connection() as conn:
            conn.execute("DELETE FROM categories WHERE id = 1")

def test_customers(db):
    assert db.add_customer("Alice", "1234567890") is True
    assert db.add_customer("Bob", "1234567890") is False # Duplicate phone
    assert len(db.get_customers()) == 1

def test_insights_data(db):
    db.add_category("Food")
    db.add_menu_item(1, "Pizza", 10.0)
    oid = db.create_order(None, "Takeaway")
    db.add_order_item(oid, 1, 1, 10.0)
    db.update_order_payment(oid, 10.0, 0, 0, 10.0, "Cash")

    cat_sales = db.get_sales_by_category()
    assert len(cat_sales) == 1
    assert cat_sales[0]['total_sales'] == 10.0

    top = db.get_top_selling_items()
    assert top[0]['name'] == "Pizza"
