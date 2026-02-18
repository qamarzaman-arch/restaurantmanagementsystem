from src.database.db_manager import DatabaseManager
import os

def test_db():
    db_path = "test_restaurant.db"
    if os.path.exists(db_path):
        os.remove(db_path)

    db = DatabaseManager(db_path)
    print(f"Database created at {db_path}")

    # Test User Authentication
    user = db.authenticate_user("admin", "admin123")
    if user:
        print(f"Authenticated admin: {user['username']} - Role: {user['role']}")
    else:
        print("Failed to authenticate admin")
        return False

    # Test Settings
    db.set_setting("currency", "USD")
    val = db.get_setting("currency")
    print(f"Setting currency: {val}")
    if val != "USD":
        print("Settings check failed")
        return False

    all_settings = db.get_all_settings()
    print(f"All settings: {all_settings}")

    # Test adding new user
    if db.add_user("staff1", "staff123", "Staff", "John Doe"):
        print("Added staff1")
    else:
        print("Failed to add staff1")
        return False

    staff = db.authenticate_user("staff1", "staff123")
    if staff and staff['full_name'] == "John Doe":
        print("Authenticated staff1 successfully")
    else:
        print("Failed to authenticate staff1")
        return False

    os.remove(db_path)
    return True

if __name__ == "__main__":
    if test_db():
        print("Database Manager Core Tests Passed!")
    else:
        print("Database Manager Core Tests Failed!")
        exit(1)
