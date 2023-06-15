import tkinter as tk
from tkinter import messagebox
import sqlite3

def create_db():
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS Stock (
            ID INTEGER PRIMARY KEY AUTOINCREMENT,
            Product TEXT NOT NULL,
            Quantity INTEGER NOT NULL,
            Store TEXT NOT NULL
        );
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            Username TEXT PRIMARY KEY,
            Password TEXT NOT NULL
        );
    ''')
    conn.commit()
    conn.close()

def validate_login(username, password):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute("SELECT * FROM Users WHERE Username = ? AND Password = ?", (username, password))
    result = c.fetchone()
    conn.close()
    if result:
        return True
    else:
        return False


def insert_data(product, quantity, store):
    conn = sqlite3.connect('stock.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO Stock (Product, Quantity, Store)
        VALUES (?, ?, ?);
    ''', (product, quantity, store))
    conn.commit()
    conn.close()

def login_window():
    window = tk.Tk()

    username_label = tk.Label(window, text="Username:")
    username_label.pack()

    username_entry = tk.Entry(window)
    username_entry.pack()

    password_label = tk.Label(window, text="Password:")
    password_label.pack()

    password_entry = tk.Entry(window, show="*")  # The show parameter replaces typed characters with asterisks for security
    password_entry.pack()

    login_button = tk.Button(window, text="Login", command=lambda: login(username_entry.get(), password_entry.get(), window))
    login_button.pack()

    window.mainloop()


def login(username, password, window):
    if validate_login(username, password):
        window.destroy()  # Close the login window
        main_window()  # Open the main window
    else:
        messagebox.showerror("Error", "Invalid username or password")


def main_window():
    window = tk.Tk()
    window.title("หวังทองดี POS system by PeePo")
    window.geometry("600x500+1000+500")

    bg_image = tk.PhotoImage(file="D:\Coding\VTDprogram\VTDpic.png") # replace with your image file path
    # Use a Label to display the image
    bg_label = tk.Label(window, image=bg_image)
    bg_label.place(x=0, y=0, relwidth=1, relheight=1)

    product_label = tk.Label(window, text="Product Name:")
    product_label.pack()

    product_entry = tk.Entry(window)
    product_entry.pack()

    quantity_label = tk.Label(window, text="Quantity:")
    quantity_label.pack()

    quantity_entry = tk.Entry(window)
    quantity_entry.pack()

    store_label = tk.Label(window, text="Store Location:")
    store_label.pack()

    store_entry = tk.Entry(window)
    store_entry.pack()

    submit_button = tk.Button(window, text="Submit", command=lambda: insert_data(product_entry.get(), quantity_entry.get(), store_entry.get()))
    submit_button.pack()

    window.mainloop()

if __name__ == "__main__":
    create_db()
    main_window()
    #login_window()

