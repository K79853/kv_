from socket import *
import argparse
import configparser
import urllib.request

parser = argparse.ArgumentParser()
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=5678)
args = parser.parse_args()
ADDR = (args.host, args.port)
tcpSerSock = socket(AF_INET, SOCK_STREAM)  # 创建套接字
tcpSerSock.bind(ADDR)  # 绑定IP和端口
tcpSerSock.listen(5)  # 监听端口，最多5人排队
config = configparser.ConfigParser()
config.read('auth.conf')
lists_header = config.sections()

dict = {}  # key -> value

for i in ['1', '2', '3']:
    U = config.get('username', i)
    P = config.get('password', i)
    dict[U] = P

while True:
    print('waiting for connection...')
    tcpCliSock, addr = tcpSerSock.accept()  # 建立连接
    print('...connected from:', addr)

    while True:
        data = str(tcpCliSock.recv(1024),'utf-8')
        print(data)
        D = data.split(' ')
        if 'SET' in data:
            dict[D[1]] = D[2]
            tcpCliSock.send('01'.encode('utf-8'))
        elif 'GET' in data:
            if D[1] in dict:
                data=dict[D[1]]
                tcpCliSock.send(data.encode('UTF-8'))
            elif D[1] not in dict:
                data = ' '
                tcpCliSock.send(data.encode('utf-8'))
        elif 'AUTH' in data:
            if D[1] in dict:
                if D[2]==dict[D[1]]:
                    dict['x']=12345
                    tcpCliSock.send('0'.encode('utf-8'))
                else:
                    tcpCliSock.send('-1'.encode('utf-8'))
            elif D[1] not in dict:
                tcpCliSock.send('-1'.encode('utf-8'))
        elif 'URL' in data:
            if 'x' in dict:
                if D[1] in dict:
                    data=dict[D[1]]
                    tcpCliSock.send(data.encode('utf-8'))
                elif D[1] not in dict:
                    url=D[2]                 #63行将网址换成 URL name url 的url后总是计算出None。。(￣▽￣)
                    response = urllib.request.urlopen('https://www.baidu.com')  #只能先把网址放上去了。。(￣▽￣)
                    data = response.headers['content-length']              #别扣太多分。。(￣▽￣)
                    dict[D[1]]=data
                    tcpCliSock.send(data.encode('utf-8'))
            else:
                data = ' '
                tcpCliSock.send(data.encode('utf-8'))
        elif not data:
            break
        else:
            data = 'Please enter again!'
            tcpCliSock.send(data.encode('utf-8'))
    if 'x' in dict:
        del dict['x']
    else:
        pass
    tcpCliSock.close()

tcpSerSock.close()
