# 导包
import datetime
from socket import *

# 创建 socket 对象
udpSocket = socket(AF_INET, SOCK_DGRAM)
targetAddr = ("127.0.0.1", 3000)
# 本地主机绑定端口
udpSocket.bind(("", 8088))


# 主函数
def main():
    while True:
        # 接收信息
        msg, addrInfo = udpSocket.recvfrom(1024)
        # 收到信息后使用 utf-8 解码
        print("收到来自 %s 的信息：%s" % (addrInfo[0], msg.decode("utf-8")))
        udpSocket.sendto(datetime.datetime.now().strftime("m:%m d:%d y:%y").encode("utf-8"), targetAddr)


if __name__ == '__main__':
    main()
