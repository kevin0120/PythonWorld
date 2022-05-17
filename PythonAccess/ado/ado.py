# -*- coding: utf-8 -*-
import win32com.client

DSN = r"Provider=Microsoft.Jet.OLEDB.4.0;Data Source=../data.mdb;Persist Security Info=False"

if __name__ == '__main__':
    # 获取Connection对象
    conn = win32com.client.Dispatch('ADODB.Connection')
    # 设置ConnectionString
    conn.ConnectionString = "Provider=Microsoft.Jet.OLEDB.4.0;Data Source=../data.mdb;Persist Security Info=False"  # mdb_file为mdb文件的路径
    # 打开连接
    conn.Open()  # 这里也可以conn.Open(DSN) DSN内容和ConnectionString一致
    conn.Close()

    # 据说需要32位的python和accessDatabaseengine才可以
    # https://www.cnblogs.com/springyun/p/10147229.html
