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
        data = tcpCliSock.recv(1024)
        D = data.split(str.encode(' '))
        S = str.encode('SET')
        G = str.encode('GET')
        A = str.encode('AUTH')
        Url = str.encode('URL')
        if S in data:
            dict[str(D[1],'utf-8')] = str(D[2],'utf-8')
            tcpCliSock.send('01'.encode('utf-8'))
        elif G in data:
            if str(D[1],'utf-8') in dict:
                data=dict[str(D[1],'utf-8')]
                tcpCliSock.send(data.encode('UTF-8'))
            elif str(D[1],'utf-8') not in dict:
                data = ' '
                tcpCliSock.send(data.encode('utf-8'))
        elif A in data:
            if str(D[1],'utf-8') in dict:
                if str(D[2],'utf-8')==dict[str(D[1],'utf-8')]:
                    dict['x']=12345
                    tcpCliSock.send('0'.encode('utf-8'))
                else:
                    tcpCliSock.send('-1'.encode('utf-8'))
            elif str(D[1],'utf-8') not in dict:
                tcpCliSock.send('-1'.encode('utf-8'))
        elif Url in data:
            if 'x' in dict:
                if str(D[1],'utf-8') in dict:
                    data=dict[str(D[1],'utf-8')]
                    tcpCliSock.send(data.encode('utf-8'))
                elif str(D[1],'utf-8') not in dict:
                    url=str(D[2],'utf-8')                 #63行将网址换成 URL name url 的url后大小总是计算出None。。(￣▽￣)
                    response = urllib.request.urlopen('https://www.baidu.com')  #只能先把网址放上去了。。(￣▽￣)
                    data = response.headers['content-length']              #师兄，手下留情。。(￣▽￣)
                    dict[str(D[1],'utf-8')]=data
                    tcpCliSock.send(data.encode('utf-8'))
            else:
                data = ' '
                tcpCliSock.send(data.encode('utf-8'))
        elif not data:
            break
        else:
            data = 'Please enter again!'
            tcpCliSock.send(data.encode('utf-8'))

    del dict['x']
    tcpCliSock.close()

tcpSerSock.close()
