import psycopg2
from psycopg2.extras import DictCursor


class PgSqlHandler(object):

    def __init__(self, host, user, port, password, database):
        self.conn = psycopg2.connect(
            host=host,
            user=user,
            port=port,
            password=password,
            database=database
        )

        self.cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    def query(self, sql, one=True):
        self.cursor.execute(sql)
        self.conn.commit()
        if one:
            results = self.cursor.fetchone()
            return {key: value for key, value in results.items()}

        else:
            results = self.cursor.fetchall()
            my_list = []
            for i, v in enumerate(results):
                my_dict = {}
                for key, value in v.items():
                    my_dict[key] = value
                my_list.append(my_dict)
            return my_list
            # return [{key: value} for i, v in enumerate(results) for key, value in v.items()]

    def close(self):
        self.cursor.close()
        self.conn.close()


if __name__ == '__main__':
    from middleware import handler_middle
    db = PgSqlHandler(host=handler_middle.Handler.yml_conf['pgsql']['host'],
                      user=handler_middle.Handler.yml_conf['pgsql']['user'],
                      port=handler_middle.Handler.yml_conf['pgsql']['port'],
                      password=handler_middle.Handler.yml_conf['pgsql']['password'],
                      database='crm_admin_philips')

    # db_sql = "SELECT * FROM crm_sys_dept limit 2"
    db_sql = "SELECT * FROM crm_sys_dept where dept_no = 'DEPT0122'"

    result = db.query(db_sql, one=False)
    print(result)
