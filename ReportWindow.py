import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from database import Database

class ReportAdminWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.title("Edit Gold Stock")
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width-100}x{screen_height-100}')
        self.state('zoomed')

        self.db = Database('2403:6200:8846:62be:ced3:a061:6091:74b0', 'admin', 'adminvtd', 'vtd')

        # Create a main frame
        self.main_frame = ttk.Frame(self)
        self.main_frame.grid(sticky='nsew')

        # Create a frame for the first row
        self.row1_frame = ttk.Frame(self.main_frame)
        self.row1_frame.grid(row=0, column=0, sticky='nsew')

        self.tree_frame = ttk.Frame(self.row1_frame)
        self.tree_frame.grid(row=0, column=0, pady=20)

        self.init_tree(self.tree_frame)

        self.load_stocks_all_db()

        # Add date filter
        self.start_date = DateEntry(self.row1_frame)
        self.start_date.grid(row=2, column=0)
        self.filter_button = tk.Button(self.row1_frame, text="Filter by Date", command=self.filter_by_date)
        self.filter_button.grid(row=2, column=2)

        # Add save to PDF button
        self.pdf_button = tk.Button(self.row1_frame, text="Save to PDF", command=self.save_to_pdf)
        self.pdf_button.grid(row=2, column=3)
    
    def init_tree(self, frame):
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.grid(row=0, column=1, sticky='ns')

        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('id','วันที่','เวลา',    'เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง', 'น้ำหนักตามตามจริง'), show='headings')
        self.tree.grid(row=0, column=0, sticky='nsew')

        frame.grid_columnconfigure(0, weight=1)
        frame.grid_rowconfigure(0, weight=1)

        self.tree_scroll.config(command=self.tree.yview)

        for col in ('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร',    'น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง'):
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)

    def filter_by_date(self):
        date = self.start_date.get_date()

        # Clear the tree view
        for i in self.tree.get_children():
            self.tree.delete(i)
        for row in self.db.fetch_by_date(date):
            self.tree.insert('', 'end', values=row[0:])

    def save_to_pdf(self):
        data = []  # This should contain all data from the tree view
        c = canvas.Canvas("output.pdf", pagesize=letter)
        width, height = letter
        for i, row in enumerate(data):
            for j, item in enumerate(row):
                c.drawString(j * 100 + 50, height - i * 100 - 50, str(item))
        c.save()

    def load_stocks_all_db(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.db.fetch_all():
            self.tree.insert('', 'end', values=row[0:])