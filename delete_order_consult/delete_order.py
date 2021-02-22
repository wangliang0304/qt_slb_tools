from delete_order_consult.MysqlUtil import Mysql
from PySide2.QtWidgets import QApplication, QMessageBox
from PySide2.QtUiTools import QUiLoader
from PySide2.QtCore import QFile

def init_db():
    mysql = Mysql(
        host="rm-wz9p49j5t59q7bm7gjo.mysql.rds.aliyuncs.com",
        user="slbroot",
        password="woolconsult_86release",
        database="consult-service",
        charset="utf8",
        port=3306
    )
    return mysql

def query_customer_id(phone):
    customer_select_sql = 'SELECT id as c_id FROM `customer` c WHERE c.phone = %d;' % phone
    mysql = init_db()
    sql_result = mysql.fetch_one(customer_select_sql)
    if not sql_result is None:
        customer_id = sql_result[0]
        print(f"customer_id is :{customer_id}")
        return customer_id
    # except Exception as e:
    #     print("未知异常：",e)
    else:
        print("查customer_id的sql结果为空")

def query_order_id(customer_id):
    if not customer_id is None:
        order_select_sql = 'SELECT id as o_id FROM `order` WHERE customer_id = %d;'%customer_id
    mysql = init_db()
    sql_result = mysql.fetch_one(order_select_sql)
    if not sql_result is None:
        order_id = sql_result[0]
        print(f"order_id id :{order_id}")
        return order_id
    else:
        print("查order_id的sql结果为空")


def delete_customer(customer_id):
    if not customer_id is None:
        sql = 'delete from `customer` where id = %d;'%customer_id
    mysql = init_db()
    result=mysql.exec(sql)
    print(f"删除的数据量为：{result}")
    print(f"customer_id:{customer_id}的客户记录删除成功！")

def delete_order(order_id):
    if not order_id is None:
        sql = 'delete from `order` where id = %d;'%order_id
    mysql = init_db()
    result = mysql.exec(sql)
    print(f"删除的数据量为：{result}")
    print(f"order_id:{order_id}的订单记录删除成功！")

def set_null_wx_customer(customer_id):
    if not customer_id is None:
        sql = 'update wx_customer set customer_id = null where customer_id = %d;' % customer_id
    mysql = init_db()
    result = mysql.exec(sql)
    print(f"置空的数据量为：{result}")
    print(f"customer_id:{customer_id}的微信记录对应的customer_id已置空！")


def delete_process(phone):
    """
    作用：完全删除相关的数据流。
    前提：用户填写问卷，已创建对应customer记录。
    :param phone:
    :return:
    """
    customer_id = query_customer_id(phone)
    if not customer_id is None:
        order_id = query_order_id(customer_id)
        delete_customer(customer_id)
        set_null_wx_customer(customer_id)
    else:
        order_id = None
        print("customer_id为空，无需删除customer记录和wx_customer记录。 ")

    if not order_id is None:
        delete_order(order_id)

    print(f"已填写问卷,手机号为：{phone}的订单的相关数据已清空！")

# delete_process(15923912072)

class Delete:
    def __init__(self):
        # 从文件中动态加载UI定义
        qfile = QFile('delete_02.ui')
        qfile.open(QFile.ReadOnly)
        qfile.close()

        # 从 UI 定义中动态 创建一个相应的窗口对象
        # 注意：里面的控件对象也成为窗口对象的属性了
        # 比如 self.ui.button , self.ui.textEdit
        self.ui = QUiLoader().load(qfile)
        # self.ui
        self.ui.button.clicked.connect(self.delete)

    def delete(self):
        info = int(self.ui.textEdit.toPlainText())
        delete_process(info)



        QMessageBox.about(self.ui,
                    '删除结果',
                    f'''手机号为：{info}的订单数据已清空！'''
                    )

if __name__ == '__main__':
    app = QApplication([])
    stats = Delete()
    stats.ui.show()
    app.exec_()



