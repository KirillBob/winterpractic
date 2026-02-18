import os
import datetime
import psycopg2 as ps
import time

class Database:
    def __init__(self, database, user, password, host, port):
        self.conn = ps.connect(database=database, user=user, password=password, host=host, port=port)
        self.cur = self.conn.cursor()

    def constructor(self):
        self.cur.execute("CREATE TABLE files (" \
        "id SERIAL PRIMARY KEY, " \
        "name VARCHAR(64) NOT NULL," \
        "extension VARCHAR(64) NOT NULL," \
        "size INTEGER," \
        "path VARCHAR(64)," \
        "created_at TIMESTAMP," \
        "updated_at TIMESTAMP," \
        "comment VARCHAR(64))")
        self.conn.commit()
    
    def destructor(self):
        self.cur.execute("DELETE FROM files")
        self.conn.commit()

    def delete(self, path):
        self.cur.execute("DELETE FROM files WHERE path = %s", (path, ))
        self.conn.commit()

    def write_sql(self, dirpath, filename):
        if "." in filename:
            name = filename.split(".")[0]
            expansion = filename.split(".")[1]
        else:
            name = filename
            expansion = ""
        stats = os.stat(os.path.join(dirpath, filename))
        self.cur.execute("INSERT INTO files (name, extension, size, path, created_at, updated_at) VALUES (%s, %s, %s, %s, %s, %s)", \
        (name, expansion, stats.st_size, os.path.join(dirpath, filename), datetime.datetime.fromtimestamp(stats.st_ctime), datetime.datetime.fromtimestamp(stats.st_mtime)))
        self.conn.commit()

    def make_root(self, root):
        for dirpath, _, filenames in os.walk(root):
            for filename in filenames:
                self.write_sql(dirpath, filename)

    def update(self, name, new_path, old_path, comment):
        self.cur.execute("UPDATE files SET name = %s, path = %s, comment = %s, updated_at = %s WHERE path = %s", (name, new_path, comment, time.strftime('%Y-%m-%d %H:%M:%S'), old_path))
        self.conn.commit()

   
    def select(self, path=None, seach=None):
        if isinstance(seach, bool):
            seach_str = f"%{path}%"
            self.cur.execute("SELECT name, extension, size, path, created_at, updated_at, comment FROM files WHERE path LIKE %s", (seach_str, ))
            return self.cur.fetchall()
        elif isinstance(path, str):
            self.cur.execute("SELECT name, extension, size, path, created_at, updated_at, comment FROM files WHERE path = %s", (path, ))
            return self.cur.fetchall()
        self.cur.execute("SELECT name, extension, size, path, created_at, updated_at, comment FROM files")
        return self.cur.fetchall()
