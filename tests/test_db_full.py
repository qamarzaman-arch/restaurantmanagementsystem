from src.database.db_manager import DatabaseManager
import os

def test_full_crud():
    db_path = "test_full.db"
    if os.path.exists(db_path): os.remove(db_path)
    db = DatabaseManager(db_path)

    # Categories
    db.add_category("Starters")
    cats = db.get_categories()
    assert len(cats) == 1
    assert cats[0]['name'] == "Starters"
    cat_id = cats[0]['id']

    # Menu Items
    db.add_menu_item(cat_id, "Spring Rolls", 5.99, "Crispy rolls")
    items = db.get_menu_items()
    assert len(items) == 1
    assert items[0]['name'] == "Spring Rolls"
    item_id = items[0]['id']

    # Tables
    db.add_table("T1", 4)
    tables = db.get_tables()
    assert len(tables) == 1
    assert tables[0]['table_number'] == "T1"
    table_id = tables[0]['id']

    # Orders
    order_id = db.create_order(table_id, "Dine-in")
    db.add_order_item(order_id, item_id, 2, 5.99)
    order = db.get_order(order_id)
    assert order['status'] == 'Pending'
    assert len(order['items']) == 1
    assert order['items'][0]['name'] == "Spring Rolls"

    # Check table status
    tables = db.get_tables()
    assert tables[0]['status'] == 'Occupied'

    # Payment
    db.update_order_payment(order_id, 11.98, 0.60, 0.0, 12.58, "Cash")
    order = db.get_order(order_id)
    assert order['status'] == 'Completed'

    # Check table free
    tables = db.get_tables()
    assert tables[0]['status'] == 'Available'

    # Inventory
    db.update_inventory("Potato", 10, "kg")
    db.update_inventory("Potato", -2)
    inv = db.get_inventory()
    assert inv[0]['item_name'] == "Potato"
    assert inv[0]['quantity'] == 8

    print("Full CRUD Tests Passed!")
    os.remove(db_path)

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    test_full_crud()
