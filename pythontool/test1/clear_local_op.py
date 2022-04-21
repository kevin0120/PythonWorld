import sys
import psycopg2


def clearOP(masterip):
    print(masterip)
    conn = None
    try:
        conn = psycopg2.connect(database="rush", user="admin", password="admin", host=masterip, port="5432", connect_timeout=3)
        print(str(masterip) + ":opendb ok")
        cur = conn.cursor()
        cur.execute("delete from routing_operations;")
        conn.commit()
        print(str(masterip) + ":num of rows deleted:" + str(cur.rowcount))
        conn.close()
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


def clearOPByFile(file):
    with open(file, 'r') as f:
        while True:
            line = f.readline().strip('\n')
            if not line:
                break
            clearOP(line)


def showOP(masterip):
    conn = None
    try:
        conn = psycopg2.connect(database="rush", user="admin", password="admin", host=masterip, port="5432", connect_timeout=3)
        print(str(masterip) + ":opendb ok")
        cur = conn.cursor()
        cur.execute("select name, product_type, workcenter_code from routing_operations;")
        rows = cur.fetchall()
        for r in rows:
            print(r)
    except Exception as e:
        print(e)
    finally:
        if conn:
            conn.close()


if __name__ == "__main__":
    print(sys.argv)
    if len(sys.argv) == 1:
        print('clear_local_op.py show | del [-f]')
    else:
        if sys.argv[1] == 'show':
            if sys.argv[2]:
                showOP(sys.argv[2])
            else:
                print('clear_local_op.py show | del [-f]')
        elif sys.argv[1] == 'del':
            if sys.argv[2] == '-f':
                if sys.argv[3]:
                    clearOPByFile(sys.argv[3])
                else:
                    print('clear_local_op.py show | del [-f]')
            else:
                if sys.argv[2]:
                    clearOP(sys.argv[2])
                else:
                    print('clear_local_op.py show | del [-f]')
        else:
            print('clear_local_op.py show | del [-f]')
