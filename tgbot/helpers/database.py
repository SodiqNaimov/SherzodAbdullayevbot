import sqlite3
# from tgbot.files.config import db_path

# database = sqlite3.connect(db_path)
# cursor = database.cursor()


class SQLite:
    def __init__(self, database):
        self.connection = sqlite3.connect(database)
        self.cursor = self.connection.cursor()

    def register_user(self, user_id,full_name,age,address,payment):
        with self.connection:
            self.connection.execute("""INSERT INTO users (user_id,full_name,age,address,payment) VALUES
            (?, ?, ?,?,?)""", [user_id,full_name,age,address,payment])

    def is_registered(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT user_id FROM users WHERE user_id == ? """, [user_id])
            rows = self.cursor.fetchall()

            return rows

    def get_user_info(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT full_name,age,address FROM users WHERE user_id == ? """, [user_id])
            row = self.cursor.fetchall()[0]

            return row

    def payment_yes(self):
        with self.connection:
            self.cursor.execute("""SELECT payment FROM users WHERE payment == ? """, ["Ha"])
            row = self.cursor.fetchall()

            return row
    def payment_no(self):
        with self.connection:
            self.cursor.execute("""SELECT payment FROM users WHERE payment == ? """, ["Yo'q"])
            row = self.cursor.fetchall()

            return row
    def count_of_user(self):
        with self.connection:
            self.cursor.execute("""SELECT user_id FROM users""")
            row = self.cursor.fetchall()

            return row

    def all_payment(self):
        with self.connection:
            self.cursor.execute("SELECT payment FROM users")
            row = self.cursor.fetchall()

            return row

    def update_user_payment(self, user_id, payment, date, end_payment):
        with self.connection:
            self.cursor.execute("""UPDATE users SET payment =?,date =?,end_payment=? WHERE user_id = ? """, (payment, date,end_payment,user_id))

    def get_all_user_info(self):
        with self.connection:
            self.cursor.execute("""SELECT full_name,age,address,payment,date,end_payment FROM users """)
            row = self.cursor.fetchall()

            return row

    def get_pay_users(self):
        with self.connection:
            self.cursor.execute("""SELECT user_id FROM users WHERE payment = ?""", ['Ha'])
            row = self.cursor.fetchall()

            return row

    def check_term(self):
        with self.connection:
            self.cursor.execute("""SELECT user_id, end_payment FROM users WHERE payment = ?""", ['Ha'])
            row = self.cursor.fetchall()

            return row

    def update_user_not_payment(self, user_id):
        with self.connection:
            self.cursor.execute("""UPDATE users SET payment =?,date =?,end_payment=? WHERE user_id = ? """, ("Yo'q", None, None, user_id))

    def get_user_pay(self, user_id):
        with self.connection:
            self.cursor.execute("""SELECT end_payment FROM users WHERE payment = ? and user_id = ?""", ['Ha', user_id])
            row = self.cursor.fetchone()

        return row
# cursor.execute("""CREATE TABLE users (
#            user_id       int      not null,
#            full_name     text     not null,
#            age     int     not null,
#             address  text  not null,
#             payment   text  not null,
#             date    date not null)
#            """)

""" 
    lang == int: 0 => uz; 1 => ru; 2 => en
"""
