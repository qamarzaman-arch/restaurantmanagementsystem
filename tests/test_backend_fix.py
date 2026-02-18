from src.database.db_manager import DatabaseManager
import sqlite3
import os

def test_fk():
    db_path = "test_fk.db"
    if os.path.exists(db_path): os.remove(db_path)
    db = DatabaseManager(db_path)

    db.add_category("Test Cat")
    db.add_menu_item(1, "Test Item", 10.0)

    # Try to delete category - should fail if FK is enforced
    try:
        with db.get_connection() as conn:
            conn.execute("DELETE FROM categories WHERE id = 1")
        print("FK violation: Category deleted even with items!")
        return False
    except sqlite3.IntegrityError:
        print("FK enforced successfully.")

    os.remove(db_path)
    return True

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    if test_fk():
        print("Database Backend Fixes Verified!")
    else:
        exit(1)
