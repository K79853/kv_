from socket import *
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host',default='127.0.0.1')
parser.add_argument('--port',type=int,default=5678)
args = parser.parse_args()
ADDR = (args.host,args.port)

tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

while True:
    data = input('请输入命令： ')
    if not data:
        break

    tcpCliSock.send(data.encode("utf-8"))
    data = tcpCliSock.recv(1024)
    if data.decode("utf-8")=='01':  #检测SET命令
        pass
    elif data.decode("utf-8")=='0':  #检测AUTH登陆成功
        print('0')
    elif data.decode("utf-8")=='-1':  #检测AUTH登录失败
        print('-1')
    else:
        print(data.decode("utf-8"))

tcpCliSock.close()
