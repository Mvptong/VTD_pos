import mysql.connector

class Database:
    def __init__(self, host, user, password, db):
        self.conn = mysql.connector.connect(host=host, user=user, password=password, database=db)
        self.cur = self.conn.cursor()

    def fetch(self):
        self.cur.execute("SELECT transaction_id, Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real, qtt_doc - qtt_real as qttdiff, weight_doc - weight_real as weightdiff, is_checked  FROM gold_stock WHERE Date = CURDATE()")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_all(self):
        self.cur.execute("SELECT transaction_id, Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real, qtt_doc - qtt_real as qttdiff, weight_doc - weight_real as weightdiff  FROM gold_stock ")
        rows = self.cur.fetchall()
        return rows
    
    def fetch_by_date(self,date):
        self.cur.execute(f"SELECT transaction_id, Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real, qtt_doc - qtt_real as qttdiff, weight_doc - weight_real as weightdiff  FROM gold_stock WHERE date = '{date}'")
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
    
    def fetch_by_userafteredit(self, username):
        self.cur.execute("SELECT * FROM gold_stock WHERE user=%s AND is_checked !=1 AND Date = CURDATE()", (username,))
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

    def update(self,id_, Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real, is_checked):
        
        self.cur.execute("""
            UPDATE gold_stock SET Date=%s,
            Time=%s,
            id_manu=%s,
            branch=%s,
            user=%s,
            product=%s,
            qtt_doc=%s,
            weight_doc=%s,
            qtt_real=%s,weight_real=%s , is_checked=%s WHERE transaction_id=%s""",
                         (Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real, is_checked, id_))
        
        self.conn.commit()
    
    def update2(self,id_, Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real):
        
        self.cur.execute("""
            UPDATE gold_stock SET Date=%s,
            Time=%s,
            id_manu=%s,
            branch=%s,
            user=%s,
            product=%s,
            qtt_doc=%s,
            weight_doc=%s,
            qtt_real=%s,weight_real=%s WHERE transaction_id=%s""",
                         (Date, Time, id_manu, branch, user, product, qtt_doc, weight_doc, qtt_real, weight_real, id_))
        
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
