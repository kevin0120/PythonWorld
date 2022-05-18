# -*-coding:utf-8-*-

import time
from PythonAccess.odbc.tangche.utils import util
from loguru import logger

logger.add("logs/tangche_press.log", rotation="1 days", level="INFO", encoding='utf-8')  # 文件日誌
# logger.add(sys.stderr, format="{time} {level} {message}", level="INFO")

logger.info('系统启动！！！')


if __name__ == '__main__':
    logger.info(util.args)
    while 1 == 1:
        try:
            util.readFromDbAndSend()
        except:
            logger.info('read db fail')
            time.sleep(util.args.t)
            continue
        else:
            logger.info('read db success')
        time.sleep(util.args.pt)
