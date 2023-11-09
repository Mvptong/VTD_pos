from gold_stock_app import GoldStockApp
from utils import hash_password
from database import Database
import socket

hostname = socket.gethostname()


# Create and start the application
if __name__ == "__main__":
    # Create a database object
    
    if hostname == 'Chanawee_PC':
        db = Database('localhost', 'admin', 'adminvtd', 'vtd')
    else:
        db = Database('2403:6200:8846:62be:ced3:a061:6091:74b0', 'admin', 'adminvtd', 'vtd')

    # Now launch the GUI
    app = GoldStockApp()
    app.mainloop()
