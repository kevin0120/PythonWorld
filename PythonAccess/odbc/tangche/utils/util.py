import argparse
import json
import threading
from datetime import datetime
from loguru import logger
import pyodbc
import requests

parser = argparse.ArgumentParser(description="This is a example program ")
parser.add_argument("-n", type=int, default=2, dest='n', help="每次读取压机数据的条数")

parser.add_argument("-pt", type=int, default=5, dest='pt', help="两次读取压机数据的时间间隔")
# parser.add_argument("echo", help="echo the string")

parser.add_argument("-db", type=str, default=r'D:\Code\lianxi\PythonWorld\PythonAccess\data1.mdb', dest='db',
                    help="数据库路径")
parser.add_argument("-odoo", type=str, default=r'127.0.0.1', dest='odoo',
                    help="odoo后台ip")
parser.add_argument("-rush", type=str, default=r'127.0.0.1', dest='rush',
                    help="rush后台ip")

parser.add_argument("-sn", type=str, default=r'001100', dest='sn',
                    help="压机序列号")
parser.add_argument("-t", type=float, default=0.1, dest='t',
                    help="压机采样周期")

parser.add_argument("-data", type=str, default=r'', dest='data',
                    help="压机功能缓存数据")

args = parser.parse_args()

pressData = {'press_value': [], 'press_time': []}
headers = {
    "content-type": "application/json"
}

def readFromDbAndSend():
    # 连接数据库（不需要配置数据源）,connect()函数创建并返回一个 Connection 对象
    connstr = r'DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=' + args.db

    cnxn = pyodbc.connect(connstr)
    # cursor()使用该连接创建（并返回）一个游标或类游标的对象
    crsr = cnxn.cursor()

    right = True
    for row in crsr.execute("SELECT top {} * from data order by cdate(压装时间) desc ".format(args.n)):
        # print(row)
        pressSignalData = {'cur_m': [], 'cur_w': [], 'cur_t': []}
        result = tuple(row)
        # 压机序列号
        pressData['press_sn'] = args.sn
        # 压装时间
        pressData['press_time'].insert(0, float(result[6]))
        # 保压值
        pressData['press_value'].insert(0, float(result[11][:result[11].index("KN")]))
        # 文件名
        pressData['press_file'] = result[2] + "-" + datetime.strptime(result[7], "%Y-%m-%d %H:%M:%S").strftime(
            "%Y%m%d%H%M")
        # 轴型
        pressData['axis_type'] = result[1]
        # 轴号
        pressData['axis_sn'] = result[3]

        # 轴承的相应信息
        # 轴承型号
        pressSignalData['bearing_type'] = result[4]
        # 压装力
        pressSignalData['power_on'] = float(result[9])
        # 贴合力
        pressSignalData['power_keep'] = float(result[8][:result[8].index("KN")])
        # 轴承编号
        pressSignalData['bearing_sn'] = result[5]
        # 压装结果
        pressSignalData['result'] = result[11][result[11].index("/") + 1:]

        # 压装力
        pressSignalData['cur_m'] = [float(i) for i in result[14].split(",")]
        # 压装距离
        pressSignalData['cur_w'] = [float(i) for i in result[15].split(",")]
        # 压装时间
        pressSignalData['cur_t'] = [float(i) * args.t for i in range(len(result[14].split(",")))]
        if right:
            right = False
            # 右侧压装数据
            pressData['right'] = pressSignalData
        else:
            # 左侧压装数据
            right = True
            pressData['left'] = pressSignalData

    # print(json.dumps(pressData, indent=2))
    logger.info(u"成功从数据库中读取一条记录:{}".format(json.dumps(pressData)))
    crsr.commit()
    crsr.close()
    cnxn.close()
    httpSend()


def httpSend():
    t1 = threading.Thread(target=rushStatus, args=())
    t2 = threading.Thread(target=rushSendData, args=())
    t3 = threading.Thread(target=odooSendData, args=())
    t1.start()
    t2.start()
    t3.start()


def rushStatus():
    try:
        r = requests.post("http://{}:8082/rush/v1/statusPress".format(args.rush), headers=headers,
                          data=json.dumps(pressData))
        logger.info(u"发送成功rushStatus:{}".format(r.text))
    except Exception as e:
        logger.error("发送失败rushStatus:{}".format(e))
        return


def rushSendData():
    try:
        r = requests.post("http://{}:8082/rush/v1/recvPress".format(args.rush), headers=headers,
                          data=json.dumps(pressData))
        logger.info(u"发送成功rushSendData:{}".format(r.text))
    except Exception as e:
        logger.error("发送失败rushSendData:{}".format(e))
        return


def odooSendData():
    try:
        if pressData['press_file'] == args.data:
            logger.info(u"已成功发送过odooSendData:{}  不再重复发送".format(args.data))
            return
        r = requests.post("http://{}:8069/ts031/recvPress".format(args.odoo), headers=headers,
                          data=json.dumps(pressData))
        if r.status_code == 200:
            args.data = pressData['press_file']
            logger.info(u"发送成功odooSendData:{}".format(r.text))
    except Exception as e:
        logger.error("发送失败odooSendData:{}".format(e))
        return
