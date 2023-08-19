import tkinter as tk
from tkinter import ttk

class GoldStockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('ห้างทองหวังทองดี')
        
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
    
    def init_main_interface(self):
        self.tree_frame = ttk.Frame(self.main_frame)
        self.tree_frame.pack(pady=20)
        
        self.init_tree(self.tree_frame)
        
        self.add_button = tk.Button(self.main_frame, text="Add Gold", command=self.show_add_gold_interface)
        self.add_button.pack(pady=20)
        
        self.edit_button = tk.Button(self.main_frame, text="Edit Gold Stock", command=self.edit_gold_stock)
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
        
    def show_add_gold_interface(self):
        self.main_frame.pack_forget()
        self.add_frame.pack(fill="both", expand=True)
        
    def add_gold_to_table(self):
        values = [self.entries[col].get() for col in ('วันที่', 'SKU', 'หยิบทองที่', 'ประเภท', 'น้ำหนัก', 'จำนวน', 'User', 'สถานะ')]
        self.tree.insert('', 'end', values=values)
        self.show_main_interface()

    def edit_gold_stock(self):
        EditStockWindow(self)
        
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
app = GoldStockApp()
app.mainloop()
