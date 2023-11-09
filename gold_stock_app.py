import tkinter as tk
from tkinter import ttk, font
from login_window import LoginWindow
from add_user_window import AddUserWindow
from database import Database
from EditStockWindow import EditStockAdminWindow
from tkcalendar import DateEntry
import datetime
from EditUserWindow import EditStockUserWindow
from ReportWindow import ReportAdminWindow
import socket

hostname = socket.gethostname()

class GoldStockApp(tk.Tk):
    def __init__(self):
        super().__init__()
        # Hide the main window at first
        self.withdraw()
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(size=20)
        self.title('ห้างทองหวังทองดี')
        # ... (your original __init__ code for GoldStockApp)
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry(f'{screen_width-100}x{screen_height-100}')

        self.main_frame = ttk.Frame(self)
        self.add_frame = ttk.Frame(self)

        self.init_main_interface()
        self.init_add_gold_interface(hostname)
        
        #self.show_main_interface()
        # Creating Database instance
        
        if hostname == 'Chanawee_PC':
            self.db = Database('localhost', 'admin', 'adminvtd', 'vtd')
        else:
            self.db = Database('2403:6200:8846:62be:ced3:a061:6091:74b0', 'admin', 'adminvtd', 'vtd')

        self.user_data = {user[0]: user[2] for user in self.db.fetch_users()}


        self.login_window = LoginWindow(self)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.load_stocks_from_db()
        
    def login_success(self, role, username):
        # Show the main window
        self.state('zoomed')
        self.deiconify()
        if role == 1:
            self.add_user_button = tk.Button(self.main_frame, text="Add User", command=self.show_add_user_interface)
            self.add_user_button.pack(pady=20)
            self.refresh_button = tk.Button(self.main_frame, text="รีเฟรช", command=self.load_stocks_from_db)
            self.refresh_button.pack(pady=20)
            self.report_button = tk.Button(self.main_frame, text="ดูรีพอร์ท", command=self.show_report_admin_interface)
            self.report_button.pack(pady=20)
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
        
        self.add_button = tk.Button(self.main_frame, text="ลงทอง", command=self.show_add_gold_interface)
        self.add_button.pack(pady=20)
        
        self.edit_button = tk.Button(self.main_frame, text="แก้ไขรายการทอง", command=self.edit_gold_stock)
        self.edit_button.pack(pady=20)

        self.edituser_button = tk.Button(self.main_frame, text="เช็ครายการทอง", command=self.edit_gold_by_user)
        self.edituser_button.pack(pady=20)

    
    def show_add_user_interface(self):
        AddUserWindow(self)
    
    def show_report_admin_interface(self):
        ReportAdminWindow(self)

    def filter_stocks_by_user(self, username):
        for item in self.tree.get_children():
            values = self.tree.item(item, 'values')
            if values[5] != username :
                self.tree.delete(item)
            if values[13] == '1':
                self.tree.delete(item)
    
    def init_tree(self, frame):
        self.tree_scroll = ttk.Scrollbar(frame)
        self.tree_scroll.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.tree = ttk.Treeview(frame, yscrollcommand=self.tree_scroll.set, columns=('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง','ส่วนต่างจำนวน', 'ส่วนต่างน้ำหนัก', 'เช็ค'), show='headings', height = 12)
        self.tree.pack(pady=20)
        
        self.tree_scroll.config(command=self.tree.yview)
        
        for col in ('id','วันที่','เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร','จำนวนตามจริง','น้ำหนักตามตามจริง','ส่วนต่างจำนวน', 'ส่วนต่างน้ำหนัก','เช็ค'):
            self.tree.column(col, width=100)
            self.tree.heading(col, text=col)
    
    def init_add_gold_interface(self, hostname):
        if hostname == 'Chanawee_PC':
            self.db = Database('localhost', 'admin', 'adminvtd', 'vtd')
        else:
            self.db = Database('2403:6200:8846:62be:ced3:a061:6091:74b0', 'admin', 'adminvtd', 'vtd')
    
        self.entries = {}
    
        # Add a DateEntry for the 'date' field
        date_label = tk.Label(self.add_frame, text='Date:')
        date_label.grid(row=0, column=0, pady=10, padx=(10, 0), sticky='e')
        date_entry = DateEntry(self.add_frame, date_pattern='dd/mm/y', font=("Helvetica", 20))
        date_entry.grid(row=0, column=1, pady=10, padx=(0, 10), sticky='w')
        self.entries['วันที่'] = date_entry
    
        # Add a Label and Entry for the 'time' field
        time_label = tk.Label(self.add_frame, text='Time:')
        time_label.grid(row=1, column=0, pady=10, padx=(10, 0), sticky='e')
        time_entry = tk.Entry(self.add_frame, font=("Helvetica", 20))
        time_entry.grid(row=1, column=1, pady=10, padx=(0, 10), sticky='w')
        self.entries['เวลา'] = time_entry
    
        user_label = tk.Label(self.add_frame, text='ผู้ตรวจ:')
        user_label.grid(row=2, column=0, pady=10, padx=(10, 0), sticky='e')
        user_entry = ttk.Combobox(self.add_frame, values=self.db.fetch_usernames(), font=("Helvetica", 20))
        user_entry.grid(row=2, column=1, pady=10, padx=(0, 10), sticky='w')
        self.entries['ผู้ตรวจ'] = user_entry
    
        for i, col in enumerate(('เลขที่อ้างอิงผู้ผลิต', 'สาขา', 'สินค้า', 'จำนวนตามเอกสาร', 'น้ำหนักตามเอกสาร')):
            label = tk.Label(self.add_frame, text=col + ':')
            label.grid(row=i + 3, column=0, pady=10, padx=(10, 0), sticky='e')
            entry = tk.Entry(self.add_frame, font=("Helvetica", 20))
            entry.grid(row=i + 3, column=1, pady=10, padx=(0, 10), sticky='w')
            self.entries[col] = entry
    
        # Center all columns
        for i in range(2):  # Assuming there are 2 columns
            self.add_frame.grid_columnconfigure(i, weight=1)
    
    
        submit_frame = tk.Frame(self.add_frame, width=100)
        submit_frame.grid(row=i + 7, column=0, columnspan=2, pady=20, padx=(10, 10))
        submit_frame.grid_propagate(False)  # Prevents the frame to resize to fit its contents
        self.submit_btn = tk.Button(submit_frame, text="Add Stock", command=self.add_gold_to_table)
        self.submit_btn.pack(fill='both', expand=True)  # Makes the button fill the frame

        back_frame = tk.Frame(self.add_frame, width=100)
        back_frame.grid(row=i + 8, column=0, columnspan=2, pady=20, padx=(10, 10))
        back_frame.grid_propagate(False)
        self.back_btn = tk.Button(back_frame, text="Back", command=self.show_main_interface)
        self.back_btn.pack(fill='both', expand=True)






    def show_add_gold_interface(self):
        # Clear all entries
        for entry in self.entries.values():
            entry.delete(0, 'end')
    
        # Set current date and time
        self.entries['วันที่'].set_date(datetime.date.today())
        self.entries['เวลา'].delete(0, 'end')
        self.entries['เวลา'].insert(0, datetime.datetime.now().strftime("%H:%M:%S"))
    
        self.main_frame.pack_forget()
        self.add_frame.pack(fill="both", expand=True)

        
    def show_main_interface(self):
        self.add_frame.pack_forget()
        self.main_frame.pack(fill="both", expand=True)
        
    def add_gold_to_table(self):
        # Get the date as a string
        values = [self.entries['วันที่'].get_date().isoformat()]
        values += [self.entries[col].get() for col in ('เวลา','เลขที่อ้างอิงผู้ผลิต','สาขา','ผู้ตรวจ','สินค้า','จำนวนตามเอกสาร','น้ำหนักตามเอกสาร')]
        self.db.insert(*values)
        self.load_stocks_from_db()
        self.show_main_interface()


    def edit_gold_stock(self):
        EditStockAdminWindow(self)

    def edit_gold_by_user(self):
        EditStockUserWindow(self)

    def load_stocks_from_db(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.db.fetch():
            self.tree.insert('', 'end', values=row[0:])

    def load_stocks_from_db_user(self,user):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in self.db.fetch_by_userafteredit(user):
            self.tree.insert('', 'end', values=row[0:])
