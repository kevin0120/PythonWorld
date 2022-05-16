# -*-coding:utf-8-*-
import pyodbc

if __name__ == '__main__':
    # 连接数据库（不需要配置数据源）,connect()函数创建并返回一个 Connection 对象
    cnxn = pyodbc.connect(r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=../data.mdb')
    # cursor()使用该连接创建（并返回）一个游标或类游标的对象
    crsr = cnxn.cursor()

    # 打印数据库goods.mdb中的所有表的表名
    print('`````````````` goods ``````````````')
    for table_info in crsr.tables(tableType='TABLE'):
        print(table_info.table_name)

    # l = crsr.execute("SELECT * from data WHERE 轮对号='1111'")  # [('0001', '扇叶', 20, 'A公司', 'B公司', 2000, 2009)]

    for row in crsr.execute("SELECT top 1 * from data order by 压装时间 desc "):
        print(row)

    # rows = crsr.execute("SELECT currentStock from goods")  # 返回的是一个元组
    # for item in rows:
    #     print(item)

    # l = crsr.execute("UPDATE users SET username='lind' WHERE password='123456'")
    # print(crsr.rowcount)  # 想知道数据修改和删除时，到底影响了多少条记录，这个时候你可以使用cursor.rowcount的返回值。
    #
    # # 修改数据库中int类型的值
    # value = 10
    # SQL = "UPDATE goods " \
    #       "SET lowestStock=" + str(value) + " " \
    #                                         "WHERE goodsId='0005'"
    #
    # # 删除表users
    # crsr.execute("DROP TABLE users")
    # # 创建新表 users
    # crsr.execute('CREATE TABLE users (login VARCHAR(8),userid INT, projid INT)')
    # # 给表中插入新数据
    # crsr.execute("INSERT INTO users VALUES('Linda',211,151)")
    #
    # ''''''
    # # 更新数据
    # crsr.execute("UPDATE users SET projid=1 WHERE userid=211")
    #
    # # 删除行数据
    # crsr.execute("DELETE FROM goods WHERE goodNum='0001'")
    #
    # # 打印查询的结果
    # for row in crsr.execute("SELECT * from users"):
    #     print(row)

    # 提交数据（只有提交之后，所有的操作才会对实际的物理表格产生影响）
    crsr.commit()
    crsr.close()
    cnxn.close()
