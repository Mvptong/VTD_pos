import tkinter as tk
from tkinter import ttk, messagebox
from database import Database
import hashlib
import hashlib

def hash_password(password: str) -> str:
    """Hashes a password for secure storage."""
    return hashlib.sha256(password.encode()).hexdigest()


class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Login")
        
        # Set window size
        self.window_width = 400  # Updated width for LoginWindow
        self.window_height = 300  # Updated height for LoginWindow
        
        # Get screen size
        self.screen_width = self.winfo_screenwidth()
        self.screen_height = self.winfo_screenheight()
        
        # Calculate position to center the window on the screen
        self.x_cordinate = int((self.screen_width/2) - (self.window_width/2))
        self.y_cordinate = int((self.screen_height/2) - (self.window_height/2))
        
        # Set the geometry of the window with calculated coordinates
        self.geometry("{}x{}+{}+{}".format(self.window_width, self.window_height, self.x_cordinate, self.y_cordinate))

        self.label_username = tk.Label(self, text="Username")
        self.label_password = tk.Label(self, text="Password")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.label_username.pack(pady=20)  # Increased padding for better layout
        self.entry_username.pack(pady=20)
        self.label_password.pack(pady=20)
        self.entry_password.pack(pady=20)

        self.button_login = tk.Button(self, text="Login", command=self.validate_login)
        self.button_login.pack(pady=20)

    def validate_login(self):
        username = self.entry_username.get()
        hashed_password = hash_password(self.entry_password.get())

        user = self.master.db.fetch_user_by_username(username)
        if user and user[1] == hashed_password:  # assuming the order is username, hashed_password, role in the database
            role = user[2]
            self.master.login_success(role, username)
            self.destroy()
            return

        messagebox.showerror("Invalid Credentials", "Invalid username or password")



class AddUserWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Add User")
        
        self.label_username = tk.Label(self, text="Username")
        self.label_password = tk.Label(self, text="Password")
        self.label_role = tk.Label(self, text="Role (Admin/Normal)")
        
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")
        self.entry_role = tk.Entry(self)

        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)
        self.label_role.pack(pady=10)
        self.entry_role.pack(pady=10)

        self.button_add = tk.Button(self, text="Add User", command=self.add_user)
        self.button_add.pack(pady=10)

    def add_user(self):
        new_username = self.entry_username.get()
        new_password = hash_password(self.entry_password.get())  # hash the password before storing
        new_role = self.entry_role.get()

        if new_role not in ['Admin', 'Normal']:
            messagebox.showerror("Invalid Role", "Role must be Admin or Normal")
            return

        # Check in the database if the username already exists
        existing_user = self.master.db.fetch_user_by_username(new_username)
        if existing_user:
            messagebox.showerror("User Exists", "User with this username already exists")
            return

        # Add the new user to the database
        self.master.db.add_user(new_username, new_password, new_role)
        messagebox.showinfo("Success", "User added successfully!")
        self.destroy()


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
        
        self.show_main_interface()
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
            self.show_main_interface(username)


    def on_closing(self):
        if self.login_window:
            self.login_window.destroy()
        self.destroy()
        
    def init_main_interface(self, username=None):
        # ... (your original init_main_interface code for GoldStockApp)
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(pady=20)
        
        self.init_tree(self.tree_frame)
        
        self.add_button = tk.Button(self.main_frame, text="Add Gold", command=self.show_add_gold_interface)
        self.add_button.pack(pady=20)
        
        self.edit_button = tk.Button(self.main_frame, text="Edit Gold Stock", command=self.edit_gold_stock)
        self.edit_button.pack(pady=20)

        if username:
            self.filter_stocks_by_user(username)
        else:
            self.add_user_button = tk.Button(self.main_frame, text="Add User", command=self.show_add_user_interface)
            self.add_user_button.pack(pady=20)
            
    def show_add_user_interface(self):
        AddUserWindow(self)

    def filter_stocks_by_user(self, username):
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values[6] != username:
                self.tree.delete(item)
    
    def init_tree(self, frame):
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ'), show='headings')
        self.tree.pack(pady=20)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        for col in ('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ'):
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)
    
    def show_add_gold_interface(self):
        self.main_frame.pack_forget()
        self.add_frame.pack(fill="both", expand=True)
    
    def init_add_gold_interface(self):
        self.entries = {}
        
        for col in ('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ'):
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
        values = [self.entries[col].get() for col in ('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ')]
        self.db.insert(*values)
        self.load_stocks_from_db()
        self.show_main_interface()


    def edit_gold_stock(self):
        EditStockWindow(self)

    def load_stocks_from_db(self):
        for row in self.db.fetch():
            self.tree.insert('', 'end', values=row[1:])


# ... (your original EditStockWindow and EditStockDetailsWindow classes)
class EditStockWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Edit Gold Stock")
        
        self.tree_frame = ttk.Frame(self)
        self.tree_frame.pack(pady=20)
        
        self.init_tree(self.tree_frame)
        
        self.load_stocks_from_master()
        
        self.edit_button = tk.Button(self, text="Edit Selected Stock", command=self.edit_selected_stock)
        self.edit_button.pack(pady=20)
    
    def init_tree(self, frame):
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ'), show='headings')
        self.tree.pack(pady=20)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        for col in ('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ'):
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)
        
    def load_stocks_from_master(self):
        for item in self.master.tree.get_children():
            values = self.master.tree.item(item, 'values')
            self.tree.insert('', 'end', values=values)
    
    def edit_selected_stock(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')
        EditStockDetailsWindow(self, selected_item, *values)
        
class EditStockDetailsWindow(tk.Toplevel):
    def __init__(self, master, selected_item, *initial_values):
        super().__init__(master)
        self.master = master
        self.selected_item = selected_item

        self.title("Edit Stock Details")
        
        self.entries = {}
        
        for col, val in zip(('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ'), initial_values):
            label = tk.Label(self, text=col)
            label.pack(pady=10)
            entry = tk.Entry(self)
            entry.pack(pady=10)
            entry.insert(0, val)
            self.entries[col] = entry
        
        save_edit_btn = tk.Button(self, text="Save Edit", command=self.save_edited_gold)
        save_edit_btn.pack(pady=20)
    
    def save_edited_gold(self):
        new_values = [self.entries[col].get() for col in ('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ')]
        self.db.update(self.selected_item, *new_values)
        self.load_stocks_from_db()
        self.destroy()


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
