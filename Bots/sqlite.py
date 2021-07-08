import sqlite3 as sq


class SQLiter:

    def __init__(self, name):
        self.file_data = sq.connect(name, check_same_thread=False)
        self.cur = self.file_data.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users_alarm_info (
            user_id INTEGER,
            time TEXT 
            )''')

    def check_user(self, user_id, time):
        return len(self.cur.execute(f"SELECT user_id FROM users_alarm_info WHERE user_id={user_id} AND time='{time}'").fetchall()) == 0

    def add_user(self, user_id, time):
        if self.check_user(user_id, time):
            self.cur.execute(f'''INSERT INTO users_alarm_info VALUES({user_id}, '{time}')''')
            self.file_data.commit()

    def del_user(self, user_id, time):
        self.cur.execute(f"DELETE FROM users_alarm_info WHERE user_id={user_id} AND time='{time}'")
        self.file_data.commit()

    def get_time(self, time):
        return self.cur.execute(f"SELECT * FROM users_alarm_info WHERE time='{time}'").fetchall()

    def __del__(self):
        self.file_data.close()
