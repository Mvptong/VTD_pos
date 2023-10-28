import tkinter as tk
from tkinter import ttk
from database import Database

class EditStockAdminWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Edit Gold Stock")

        self.tree_frame = ttk.Frame(self)
        self.tree_frame.grid(row=0, column=0, pady=20)

        self.init_tree(self.tree_frame)

        self.load_stocks_from_master()

        self.edit_button = tk.Button(self, text="Edit Selected Stock", command=self.edit_selected_stock)
        self.edit_button.grid(row=1, column=0, pady=20)

        

        self.edit_entries = {}

        row_num = 2  # Starting row number for labels and entry fields

        for col in ('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง'):
            label = tk.Label(self, text=col)
            label.grid(row=row_num, column=0, pady=10, padx=(1, 1))

            entry = tk.Entry(self)
            entry.grid(row=row_num, column=2, pady=10, padx=(1, 1))
            self.edit_entries[col] = entry

            row_num += 1

        # Button to save edits
        save_edit_btn = tk.Button(self, text="Save Edit", command=self.save_edited_gold)
        save_edit_btn.grid(row=row_num, column=0, columnspan=2, pady=20)
    
    def init_tree(self, frame):
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง'), show='headings')
        self.tree.pack(pady=20)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        for col in ('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง'):
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)
        
    def load_stocks_from_master(self):
        for item in self.master.tree.get_children():
            values = self.master.tree.item(item, 'values')
            self.tree.insert('', 'end', values=values)
    
    def edit_selected_stock(self):
        selected_item = self.tree.selection()[0]
        values = self.tree.item(selected_item, 'values')

        # Display the selected stock details in the entry fields for editing
        for col, value in zip(('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง'), values):
            self.edit_entries[col].delete(0, tk.END)
            self.edit_entries[col].insert(0, value)
    
    def save_edited_gold(self):
        # Get the edited values from the entry fields
        new_values = [self.edit_entries[col].get() for col in ('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง')]
        
        # Perform the update operation on the database
        self.master.db.update(new_values[0], *new_values[1:])

        # Reload the stocks in the master tree (assuming you have a method for this)
        self.master.load_stocks_from_db()

        # Close the edit window
        self.destroy()
