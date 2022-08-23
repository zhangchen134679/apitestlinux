import pymysql
from pymysql.cursors import DictCursor


class MysqlHandler:

    def __init__(self,
                 host=None,
                 port=3306,
                 user=None,
                 password=None,
                 charset=None,
                 database="futureLoan"):

        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            password=password,
            charset=charset,
            database=database,
            cursorclass=DictCursor)

        self.cursor = self.conn.cursor()

    def query(self, sql, one=True):
        self.cursor.execute(sql)
        self.conn.commit()
        if one:
            return self.cursor.fetchone()
        else:
            return self.cursor.fetchall()

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == "__main__":
    sql_data = "select * from futureLoan.member limit 10"
    res = MysqlHandler(
        host="120.78.128.25",
        port=3306,
        user="future",
        password="123456",
        charset="utf8",
        database="futureLoan").query(sql_data)
    print(res)





















    # sql_data = "select * from futureLoan.member limit 10"
    # res = MysqlHandler(
    #     host="120.78.128.25",
    #     port=3306,
    #     user="future",
    #     password="123456",
    #     charset="utf8",
    #     database="futureLoan").query(sql_data)
    # print(res)




