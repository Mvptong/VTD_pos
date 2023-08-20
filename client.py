import tkinter as tk
from tkinter import ttk, messagebox

class LoginWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Login")
        
        self.label_username = tk.Label(self, text="Username")
        self.label_password = tk.Label(self, text="Password")
        self.entry_username = tk.Entry(self)
        self.entry_password = tk.Entry(self, show="*")

        self.label_username.pack(pady=10)
        self.entry_username.pack(pady=10)
        self.label_password.pack(pady=10)
        self.entry_password.pack(pady=10)

        self.button_login = tk.Button(self, text="Login", command=self.validate_login)
        self.button_login.pack(pady=10)

    def validate_login(self):
        username = self.entry_username.get()
        password = self.entry_password.get()

        if (username, password) in self.master.user_data:
            role = self.master.user_data[(username, password)]
            self.master.login_success(role, username)
            self.destroy()
        else:
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
        new_password = self.entry_password.get()
        new_role = self.entry_role.get()

        if new_role not in ['Admin', 'Normal']:
            messagebox.showerror("Invalid Role", "Role must be Admin or Normal")
            return
        
        if (new_username, new_password) in self.master.user_data:
            messagebox.showerror("User Exists", "User with this username and password already exists")
            return

        self.master.user_data[(new_username, new_password)] = new_role
        messagebox.showinfo("Success", "User added successfully!")
        self.destroy()

class GoldStockApp(tk.Tk):
    def __init__(self):
        super().__init__()
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

        self.user_data = {
            ('admin', 'VTDprogram2566'): 'Admin',
            # Add more users as necessary
        }

        self.login_window = LoginWindow(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        
    def login_success(self, role, username):
        if role == 'Admin':
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
        self.tree.insert('', 'end', values=values)
        self.show_main_interface()

    def edit_gold_stock(self):
        EditStockWindow(self)

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
        self.master.tree.item(self.selected_item, values=new_values)
        self.master.master.tree.item(self.selected_item, values=new_values)
        self.destroy()

# Create and start the application
if __name__ == '__main__':
    app = GoldStockApp()
    app.mainloop()
