import sqlite3

class Database:
    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS gold_stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT, 
                date TEXT, 
                manufacture TEXT, 
                product TEXT, 
                quantityDOC INT, 
                weightDOC REAL, 
                quantityREAL INT, 
                weightREAL REAL, 
                quantityDIFF INT, 
                weightDIFF REAL, 
                user TEXT, 
                note TEXT)
        """)
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS users (
                username TEXT PRIMARY KEY, 
                password TEXT, 
                role TEXT)
        """)
        self.conn.commit()

    def fetch(self):
        self.cur.execute("SELECT * FROM gold_stock")
        rows = self.cur.fetchall()
        return rows

    def fetch_users(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows

    def fetch_by_user(self, username):
        self.cur.execute("SELECT * FROM gold_stock WHERE user=?", (username,))
        rows = self.cur.fetchall()
        return rows

    def fetch_user_by_username(self, username):
        self.conn.row_factory = sqlite3.Row
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=?", (username,))
        user = cur.fetchone()
        cur.close()
        return user

    def insert_user(self, username, password, role):
        self.cur.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (username, password, role))
        self.conn.commit()

    def insert(self, date, manufacture, product, quantityDOC, weightDOC, quantityREAL, weightREAL, quantityDIFF, weightDIFF, user, note):
        self.cur.execute("""
            INSERT INTO gold_stock (date, manufacture, product, quantityDOC, weightDOC, quantityREAL, weightREAL, quantityDIFF, weightDIFF, user, note) 
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (date, manufacture, product, quantityDOC, weightDOC, quantityREAL, weightREAL, quantityDIFF, weightDIFF, user, note)
        )
        self.conn.commit()

    def remove(self, id):
        self.cur.execute("DELETE FROM gold_stock WHERE id=?", (id,))
        self.conn.commit()

    def update(self, id, date, manufacture, product, quantityDOC, weightDOC, quantityREAL, weightREAL, quantityDIFF, weightDIFF, user, note):
        self.cur.execute("""
            UPDATE gold_stock SET date=?, manufacture=?, product=?, quantityDOC=?, weightDOC=?, quantityREAL=?, weightREAL=?, quantityDIFF=?, weightDIFF=?, user=?, note=? 
            WHERE id=?""",
            (date, manufacture, product, quantityDOC, weightDOC, quantityREAL, weightREAL, quantityDIFF, weightDIFF, user, note, id)
        )
        self.conn.commit()

    def close(self):
        self.conn.close()

    def __del__(self):
        self.close()
