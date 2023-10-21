import tkinter as tk
from tkinter import ttk, messagebox
from utils import hash_password

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
        self.master.db.insert_user(new_username, new_password, new_role)
        messagebox.showinfo("Success", "User added successfully!")
        self.destroy()