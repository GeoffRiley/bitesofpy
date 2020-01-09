import sqlite3


class MovieDb:

    def __init__(self, db, data, table):
        self.con = sqlite3.connect(db)
        self.data = data
        self.table = table
        self.cur = self.con.cursor()

    def init(self):
        self._create_table()
        self._insert_sample_data()

    def _create_table(self):
        self.cur.execute(
            (f"CREATE TABLE IF NOT EXISTS {self.table}"
             "(id INTEGER PRIMARY KEY AUTOINCREMENT,"
             "title TEXT NOT NULL,"
             "year INTEGER NOT NULL,"
             "score REAL NOT NULL)")
        )

    def _insert_sample_data(self):
        self.con.executemany(
            (f"INSERT INTO {self.table} (title, year, score)"
             "VALUES (?, ?, ?)"),
            self.data)
        self.con.commit()

    def drop_table(self):
        self.cur.execute(f"DROP TABLE {self.table}")
        self.con.commit()

    def query(self, title=None, year=None, score_gt=None):
        sql = f"SELECT * FROM {self.table}"
        if title is not None:
            sql += f" WHERE title LIKE '%{title}%'"
        elif year is not None:
            sql += f" WHERE year = '{year}'"
        elif score_gt is not None:
            sql += f" WHERE score > '{score_gt}'"
        self.cur.execute(sql)
        return self.cur.fetchall()

    def add(self, title, year, score):
        self.cur.execute(
            (f"INSERT INTO {self.table} (title, year, score)"
             f" VALUES (?, ?, ?)"),
            (title, year, score)
        )
        return self.cur.lastrowid

    def delete(self, idx):
        self.cur.execute(
            f"DELETE FROM {self.table} WHERE id={idx}"
        )
