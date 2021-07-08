import sqlite3 as sq


class SQLiter:

    def __init__(self, name):
        self.file_data = sq.connect(name, check_same_thread=False)
        self.cur = self.file_data.cursor()
        self.cur.execute('''CREATE TABLE IF NOT EXISTS users_score_time_info (
            id_game INTEGER PRIMARY KEY AUTOINCREMENT,
            score INTEGER,
            time INTEGER 
            )''')

    def add_result(self, score, time):
        self.cur.execute(f"INSERT INTO users_score_time_info (score, time) VALUES ({score}, {time})")
        self.file_data.commit()

    def get_result(self):
        return self.cur.execute(f"SELECT * FROM users_score_time_info ORDER BY score DESC").fetchall()

    def __del__(self):
        self.file_data.close()
