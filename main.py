from gold_stock_app import GoldStockApp
from utils import hash_password
from database import Database



# Create and start the application
if __name__ == "__main__":
    # Create a database object
    db = Database('gold_stock.db')
    
    # Check if the admin user already exists (to avoid creating multiple admins)
    admin_user = db.fetch_user_by_username('admin')
    if not admin_user:
        # If admin doesn't exist, create one with hashed password
        hashed_admin_password = hash_password('admin')
        db.insert_user('admin', hashed_admin_password, 'Admin')

    # Now launch the GUI
    app = GoldStockApp()
    app.mainloop()
