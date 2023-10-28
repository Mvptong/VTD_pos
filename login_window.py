import tkinter as tk
from tkinter import ttk, messagebox
from utils import hash_password

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
        hashed_password = self.entry_password.get()

        user = self.master.db.fetch_user_by_username(username)
        if  user[1] == hashed_password:  # assuming the order is username, hashed_password, role in the database
            role = user[2]
            self.master.login_success(role, username)
            self.destroy()
            return

        messagebox.showerror("Invalid Credentials", "Invalid username or password")