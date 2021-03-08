import sqlite3
class SQLighter:
    def __init__(self, database_file):
        """connecting to BD"""
        self.connection = sqlite3.connect(database_file)
        self.cursor  = self.connection.cursor()

    def add_user(self, user_id):
        """add user in USERS"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `users` (`user_id`) VALUES (?)", (user_id,))

    def user_exists(self, user_id):
        """ get user from USERS"""
        with self.connection:
            result = self.cursor.execute("SELECT * FROM users WHERE user_id = ? ", (user_id,)).fetchall()
            return bool(len(result))

    def add_currency_value(self, currency, value):
        """add currency and value in in currency_value"""
        with self.connection:
            return self.cursor.execute("INSERT INTO `currency_value` (`currency`, `value`) VALUES (?, ?)", (currency, value))
    def update_currency_value(self, currency, value):
        """update cur-val in currency_value"""
        with self.connection:
            self.cursor.execute("UPDATE currency_value where value = ? WHERE currency = ? ", (value, currency))
    def get_currency_value_list(self):
        """get cur-val LIST"""
        with self.connection:
            result = self.cursor.execute("select currency, value from currency_value").fetchall()
            return result

    def get_currency_value(self, currency):
        """get cur-val VALUE"""
        with self.connection:
            result = self.cursor.execute("select value from currency_value where currency = ?", (currency,)).fetchone()
            return result



    # def get_user(self, user_id):
    #     """ check if user exists in USERS"""
    #     with self.connection:
    #         result = self.cursor.execute("SELECT * FROM users WHERE user_id = ? ", (user_id,)).fetchall()
    #         return bool(len(result))

