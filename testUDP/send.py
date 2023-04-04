# 导包
from socket import *

# 创建 socket 对象
udpSocket = socket(AF_INET, SOCK_DGRAM)
# 目标主机的 IP 和端口号
targetAddr = ("127.0.0.1", 8080)
# 本地主机绑定端口
udpSocket.bind(("", 3000))


# 主函数
def main():
    while True:
        # 接受发送的信息
        msg = input("Enter message:")
        # 发送信息 使用 utf-8 编码
        udpSocket.sendto(msg.encode("utf-8"), targetAddr)

        msg1, addrInfo = udpSocket.recvfrom(1024)
        # 收到信息后使用 utf-8 解码
        print("收到来自 %s 的信息：%s" % (addrInfo[0], msg1.decode("utf-8")))


if __name__ == '__main__':
    main()
