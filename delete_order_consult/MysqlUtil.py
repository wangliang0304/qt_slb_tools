import pymysql

# from utils.LogUtil import my_log


# 1. 创建封装类
class Mysql:
    # 2. 初始化数据，连接数据库，光标对象
    def __init__(self, host, user, password, database, charset="utf8", port=3306):
        self.conn = pymysql.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset=charset,
            port=port
        )
        # self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)  # 指定多个数据以字典返回（默认以元组数据返回）
        self.cursor = self.conn.cursor()  # 指定多个数据以字典返回（默认以元组数据返回）
        # self.log = my_log()

    # 3. 创建查询，制定方法
    def fetch_one(self, sql):
        """
        获取一条数据
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    def fetch_all(self, sql):
        """
        返回多条数据
        :param sql:
        :return:
        """
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def exec(self, sql):
        """
        执行update和delete数据
        :param sql:
        :return:
        """
        try:
            if self.cursor and self.conn:
                self.cursor.execute(sql)
                self.conn.commit()  # 执行数据后，连接对象有一个提交的操作(增删改)
        except Exception as e:
            self.conn.rollback()  # sql执行出错后的回滚操作
            print("sql执行出错")
            print(e)
            return False
        return True

    # 4. 关闭对象
    def __del__(self):
        if self.conn:
            self.conn.close()
        if self.cursor:
            self.cursor.close()


if __name__ == '__main__':
    sql_sel = "SELECT * FROM `tb_weapp_reduce_mian` WHERE user_open_id = 'oQxcN5MSlHng1_S3IaHA7eJdEu8w'"
    sql_sel_more = "SELECT * FROM `tb_weapp_reduce_mian`"
    sql = """
    SELECT * FROM wx_customer WHERE wx_name LIKE"%亮亮%";
    """
    sql_del = "DELETE FROM tb_weapp_reduce_mian WHERE user_open_id='oQxcN5MSlHng1_S3IaHA7eJdEu8w'"
    mysql = Mysql(host="rm-wz9p49j5t59q7bm7gjo.mysql.rds.aliyuncs.com",
        user="slbroot",
        password="woolconsult_86release",
        database="consult-service",
        charset="utf8",
        port=3306)
    res_one = mysql.fetch_one(sql)
    print(res_one)
    # res_more = mysql.fetch_all(sql_sel_more)
    # mysql.exec(sql_del)
    # print("数据库查询单条数据：{}".format(str(res_one)))
    # print("数据库查询{}条数据：{}".format(mysql.cursor.rowcount, str(res_more)))
    # print("数据库成功删除{}数据".format(mysql.cursor.rowcount))
    # mysql.__del__()
