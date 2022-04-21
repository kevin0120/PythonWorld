

import dataset
import time
import json

if __name__ == '__main__':
    db = dataset.connect('postgresql://odoo:odoo@localhost:5432/test')
    t = time.time()
    cur_objs = ['ttt.json']
    with db as tx:
        for i in range(1):
            q = '''SELECT create_operation_result(0, 1, timestamp '2019-01-30T07:24:26Z', 190, 1, false, 'AD', 'nok', 1, 'null', 0, 0, 'fail', 98, 0, 0.01, 1, 170, 180, 'normal', '', '', true, '1/3', 0, '_VW416_1-62-7199-01', 10, 'LVS111111', '0PC4VT')'''

            # q = ''' select * from bom_operation_rel'''

            result = tx.query(q)
            for row in result:
                print(row['create_operation_result'])
            # print(result)
        diff = time.time() - t
    print(diff)





# ## 导入psycopg2包
# import psycopg2
# ## 连接到一个给定的数据库
# conn = psycopg2.connect(database="test", user="odoo",
#                         password="odoo", host="127.0.0.1", port="5432")
# ## 建立游标，用来执行数据库操作
# cursor = conn.cursor()
#
# ## 执行SQL命令
# cursor.execute("select create_operation_result(0, 1, timestamp '2019-01-30T07:24:26Z', 190, 1, false, 'AD', 'nok', 1, 'null', 0, 0, 'fail', 98, 0, 0.01, 1, 170, 180, 'normal', '', '', true, '1/3', 0, '_VW416_1-62-7199-01', 10, 'LVS111111', '0PC4VT')")
# # cursor.execute("CREATE TABLE test_conn(id int, name text)")
# # cursor.execute("INSERT INTO test_conn values(1,'haha')")
#
# ## 提交SQL命令
# conn.commit()
#
# ## 执行SQL SELECT命令
# cursor.execute("select * from operation_result order by id desc limit(10)")
#
# ## 获取SELECT返回的元组
# rows = cursor.fetchall()
# for row in rows:
#     print('id = ', row[0], 'name = ', row[1], '\n')
#
# ## 关闭游标
# cursor.close()
#
# ## 关闭数据库连接
# conn.close()