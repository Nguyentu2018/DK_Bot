import sqlite3

conn = sqlite3.connect("data.db")
c = conn.cursor()

# tao mot table moi neu no chua co trong data
def create_table(name):
    c.execute("""CREATE TABLE IF NOT EXISTS """ + name + """(
                px REAL,
                py REAL,
                pz REAL,
                roll REAL,
                mode TEXT,
                vel REAL)""")


# nhap lieu vao table trong data
def data_entry(name):
    c.execute("""INSERT INTO """ + name + """ VALUES(?, ?, ?, ?, ?, ?)""",
              (150, 200, 301, 402, 'P', 60))
    # save
    conn.commit()

def read_from_db(name):
    c.execute("SELECT * FROM " + name)
    [print(row) for row in c.fetchall()]

def del_and_update(name):
    # c.execute("""UPDATE """ + name + """ SET px = 0, pz = 0 WHERE py = 200""")
    # c.execute("SELECT * FROM " + name)
    # [print(row) for row in c.fetchall()]
    # conn.commit()
    sql = 'DROP TABLE IF EXISTS ' + name
    c.execute(sql)
    conn.commit()
    # c.execute("SELECT * FROM " + name)
    # [print(row) for row in c.fetchall()]
def get_all_nameTableDB():
    sql = "SELECT name FROM sqlite_master WHERE type='table'"
    res = c.execute(sql)
    name = c.fetchall()
    print(name)
    return name

name = "ct1"
create_table(name)
data_entry(name)
get_all_nameTableDB()
c.close()
conn.close()