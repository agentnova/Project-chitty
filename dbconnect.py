import pymysql
class Db:
    def __init__(self):
        self.cnx = pymysql.connect(host="localhost",user="root",password="",database="chitty",port=3306)
        self.cur = self.cnx.cursor()


    def select(self, q):
        self.cur.execute(q)
        return self.cur.fetchall()

    def select_one(self, q):
        self.cur.execute(q)
        return self.cur.fetchone()
    def mid(self, q):
        self.cur.execute(q)
        f=self.cur.fetchone()

        if f[0] is  None:
            return 1
        else:
            return int(f[0])+1



    def nonreturn(self, q):             #insert, update, delete
        self.cur.execute(q)
        self.cnx.commit()
        return self.cur.lastrowid