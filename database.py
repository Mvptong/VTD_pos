import mysql.connector

class Database:
    def __init__(self, host, user, password, db):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=db)
        self.cur = self.conn.cursor()

    def fetch(self):
        self.cur.execute("SELECT Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc FROM gold_stock")
        rows = self.cur.fetchall()
        return rows

    def fetch_users(self):
        self.cur.execute("SELECT * FROM users")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_usernames(self):
        self.cur.execute("SELECT username FROM users")  # assuming 'username' is the column name
        rows = self.cur.fetchall()
        return [row[0] for row in rows]

    def fetch_by_user(self, username):
        self.cur.execute("SELECT * FROM gold_stock WHERE user=%s", (username,))
        rows = self.cur.fetchall()
        return rows

    def fetch_user_by_username(self, username):
        cur = self.conn.cursor()
        cur.execute("SELECT * FROM users WHERE username=%s", (username,))
        user = cur.fetchone()
        cur.close()
        return user


    def insert_user(self, username, password, role):
        self.cur.execute("INSERT INTO users (username, password, role) VALUES (%s, %s, %s)", (username, password, role))
        self.conn.commit()

    def insert(self, Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc):
        self.cur.execute("""
            INSERT INTO gold_stock (Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)""",
            (Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc)
            )
        self.conn.commit()

    def remove(self,id):
        self.cur.execute("DELETE FROM gold_stock WHERE id=%s", (id,))
        self.conn.commit()

    def update(self,id,date,
               manufacture,
               product,
               quantityDOC,
               weightDOC,
               quantityREAL,
               weightREAL,
               quantityDIFF,
               weightDIFF,user,
               note):
        
        self.cur.execute("""
            UPDATE gold_stock SET date=%s,
            manufacture=%s,
            product=%s,
            quantityDOC=%s,
            weightDOC=%s,
            quantityREAL=%s,
            weightREAL=%s,
            quantityDIFF=%s,
            weightDIFF=%s,user=%s
            ,note=%s WHERE id=%s""",
                         (date
                          ,manufacture
                          ,product
                          ,quantityDOC
                          ,weightDOC
                          ,quantityREAL
                          ,weightREAL
                          ,quantityDIFF
                          ,weightDIFF
                          ,user
                          ,note
                          ,id))
        
        self.conn.commit()

    def close(self):
        if hasattr(self,'cur'):
            if not self.cur.closed:
                self.cur.close()
                
        if hasattr(self,'conn'):
            if not self.conn.is_connected():
                self.conn.close()

    def __del__(self):
        if hasattr(self,'cur'):
            self.cur.close()

        if hasattr(self,'conn'):
            if self.conn.is_connected():
                self.conn.close()
