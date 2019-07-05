import sqlite3

# tao ket noi
conn = sqlite3.connect('data.db')

# khoi tao con tro
c = conn.cursor()

def CreateData(name):
    c.execute("""CREATE TABLE IF NOT EXISTS """ + name + """(
                 PX float,
                 PY integer,
                 PZ integer,
                 ROLL integer,
                 MODE integer,
                 VEL integer
                 )""")
    # # cam ket thay doi
    # conn.commit()
    # # dong ket noi
    # conn.close()


def InsetData(name):
    c.execute("""INSERT INTO """ + name + """ VALUES(255, 0, 500,0,0,0)""")

def UpdateData():
    c.execute("""UPDATE settingLoc SET ls = 1000 where name = '2'""")

def DocData():
    c.execute("SELECT ls,lh,lv,us,uh,uv FROM settingLoc where name = 'Loc1'")
    data = c.fetchall()
    print(data[0])


InsetData("chuongTrinh1")


