import tkinter as tk
from tkinter import ttk

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
        
        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('date', 'manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note'), show='headings')
        self.tree.pack(pady=20)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        for col in ('date', 'manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note'):
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
        
        for col, val in zip(('date', 'manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note'), initial_values):
            label = tk.Label(self, text=col)
            label.pack(pady=10)
            entry = tk.Entry(self)
            entry.pack(pady=10)
            entry.insert(0, val)
            self.entries[col] = entry
        
        save_edit_btn = tk.Button(self, text="Save Edit", command=self.save_edited_gold)
        save_edit_btn.pack(pady=20)
    
    def save_edited_gold(self):
        new_values = [self.entries[col].get() for col in ('date', 'manufacture', 'product', 'quantityDOC', 'weightDOC', 'quantityREAL', 'weightREAL', 'quantityDIFF', 'weightDIFF', 'user', 'note')]
        self.db.update(self.selected_item, *new_values)
        self.load_stocks_from_db()
        self.destroy()