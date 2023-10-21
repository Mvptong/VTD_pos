import tkinter as tk
from tkinter import ttk
from login_window import LoginWindow
from add_user_window import AddUserWindow
from utils import hash_password
from database import Database
from EditStockWindow import EditStockWindow
from tkcalendar import DateEntry

class GoldStockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Hide the main window at first
        self.withdraw()

        self.title('ห้างทองหวังทองดี')
        
        # ... (your original __init__ code for GoldStockApp)
        # Set window size
        self.window_width = 1000  # Updated width
        self.window_height = 500
        
        # Get screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Calculate position to center the window on the screen
        self.x_cordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_cordinate = int((self.screen_height/2) - (self.window_height/2))
        
        # Set the geometry of the window with calculated coordinates
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_cordinate, self.y_cordinate))

        self.main_frame = ttk.Frame(self)
        self.add_frame = ttk.Frame(self)

        self.init_main_interface()
        self.init_add_gold_interface()
        
        #self.show_main_interface()
        # Creating Database instance
        self.db = Database('gold_stock.db')
        self.user_data = {user[0]: user[2] for user in self.db.fetch_users()}


        self.login_window = LoginWindow(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_stocks_from_db()
        
    def login_success(self, role, username):
        # Show the main window
        self.deiconify()
        if role == 'Admin':
            self.add_user_button = tk.Button(self.main_frame, text="Add User", command=self.show_add_user_interface)
            self.add_user_button.pack(pady=20)
            self.show_main_interface()
        else:
            self.show_user_interface(username)
    
    def show_user_interface(self, username):
        #self.main_frame.pack_forget()
        #self.add_frame.pack_forget()
        self.show_main_interface()  # Display the main interface
         # Filter and show gold stocks specific to the user
        self.filter_stocks_by_user(username)
        self.add_button.pack_forget()
        self.edit_button.pack_forget()


    def on_closing(self):
        if self.login_window:
            self.login_window.destroy()
        self.destroy()
        
    def init_main_interface(self):
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(pady=20)
        
        self.init_tree(self.tree_frame)
        
        self.add_button = tk.Button(self.main_frame, text="Add Gold", command=self.show_add_gold_interface)
        self.add_button.pack(pady=20)
        
        self.edit_button = tk.Button(self.main_frame, text="Edit Gold Stock", command=self.edit_gold_stock)
        self.edit_button.pack(pady=20)

        #if username:
        #    self.filter_stocks_by_user(username)
        #else:
        #    self.add_user_button = tk.Button(self.main_frame, text="Add User", command=self.show_add_user_interface)
        #    self.add_user_button.pack(pady=20)
    
    def show_add_user_interface(self):
        AddUserWindow(self)

    def filter_stocks_by_user(self, username):
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values[10] != username:
                self.tree.delete(item)
    
    def init_tree(self, frame):
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('ID', 'date', 'manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note'), show='headings')
        self.tree.pack(pady=20)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        for col in ('ID', 'date', 'manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note'):
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)
    
    def show_add_gold_interface(self):
        self.main_frame.pack_forget()
        self.add_frame.pack(fill="both", expand=True)
    
    def init_add_gold_interface(self):
        self.entries = {}
        # Add a DateEntry for the 'date' field
        date_label = tk.Label(self.add_frame, text='date')
        date_label.pack(pady=10)
        date_entry = DateEntry(self.add_frame)
        date_entry.pack(pady=10)
        self.entries['date'] = date_entry


        for col in ('manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note'):
            label = tk.Label(self.add_frame, text=col)
            label.pack(pady=10)
            entry = tk.Entry(self.add_frame)
            entry.pack(pady=10)
            self.entries[col] = entry

        self.submit_btn = tk.Button(self.add_frame, text="Add Stock", command=self.add_gold_to_table)
        self.submit_btn.pack(pady=20)

        self.back_btn = tk.Button(self.add_frame, text="Back", command=self.show_main_interface)
        self.back_btn.pack(pady=20)
        
    def show_main_interface(self):
        self.add_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        
    def add_gold_to_table(self):
        # Get the date as a string
        values = [self.entries['date'].get_date().isoformat()]
        values += [self.entries[col].get() for col in ('manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF',  'weightDIFF', 'user', 'note')]
        self.db.insert(*values)
        self.load_stocks_from_db()
        self.show_main_interface()


    def edit_gold_stock(self):
        EditStockWindow(self)

    def load_stocks_from_db(self):
        for row in self.db.fetch():
            self.tree.insert('', 'end', values=row[0:])