# -*-coding:utf-8-*-

import time
from PythonAccess.odbc.tangche.utils import util

if __name__ == '__main__':
    print(util.args)
    while 1 == 1:
        try:
            util.readFromDbAndSend()
        except:
            print("read fail")
            time.sleep(util.args.t)
            continue
        else:
            print("read success")
        time.sleep(util.args.pt)
