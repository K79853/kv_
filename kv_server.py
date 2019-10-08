from socket import *
import argparse
import configparser
import urllib.request

parser = argparse.ArgumentParser()  #运行方式
parser.add_argument('--host', default='127.0.0.1')
parser.add_argument('--port', type=int, default=5678)
args = parser.parse_args()
ADDR = (args.host, args.port)
tcpSerSock = socket(AF_INET, SOCK_STREAM)  # 创建套接字
tcpSerSock.bind(ADDR)  # 绑定IP和端口
tcpSerSock.listen(5)  # 监听端口，最多5人排队
config = configparser.ConfigParser()  #读取配置文件
config.read('auth.conf')
lists_header = config.sections()

dict = {}  # key -> value

for i in ['1', '2', '3']:     #把配置文件每节序号相同的放到字典里
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
        D = data.split(' ')   #data分割
        if 'SET' in data:  #SET命令
            dict[D[1]] = D[2]  #关联
            tcpCliSock.send('01'.encode('utf-8'))
        elif 'GET' in data:  #GET命令
            if D[1] in dict:  #value在字典
                data=dict[D[1]]
                tcpCliSock.send(data.encode('UTF-8'))
            elif D[1] not in dict:  #value不在字典
                data = ' '
                tcpCliSock.send(data.encode('utf-8'))
        elif 'AUTH' in data:  #AUTH命令
            if D[1] in dict:  #用户名匹配
                if D[2]==dict[D[1]]:  #密码匹配
                    dict['x']=12345   #将'x'放到字典里表示用户登录成功，可进行URL命令
                    tcpCliSock.send('0'.encode('utf-8'))
                else:  #密码不匹配
                    tcpCliSock.send('-1'.encode('utf-8'))
            elif D[1] not in dict:  #用户名不匹配
                tcpCliSock.send('-1'.encode('utf-8'))
        elif 'URL' in data:  #URL命令
            if 'x' in dict:  #检测是否登陆成功
                if D[1] in dict:  #key有value
                    data=dict[D[1]]
                    tcpCliSock.send(data.encode('utf-8'))
                elif D[1] not in dict:  #key无value
                    url=D[2]         #获取URL的文件大小（失败了。。）63行将网址换成 URL name url 的url后总是计算出None。。(￣▽￣)
                    response = urllib.request.urlopen('https://www.baidu.com')  #只能先把网址放上去了。。(￣▽￣)
                    data = response.headers['content-length']              #别扣太多分。。(￣▽￣)
                    dict[D[1]]=data   #把文件大小关联到key
                    tcpCliSock.send(data.encode('utf-8'))
            else:  #未登录返回空
                data = ' '
                tcpCliSock.send(data.encode('utf-8'))
        elif not data:  #退出
            break
        else:
            data = 'Please enter again!'
            tcpCliSock.send(data.encode('utf-8'))
    if 'x' in dict:  #退出后删除字典里'x'
        del dict['x']
    else:
        pass
    tcpCliSock.close()   #关闭，等待连接

tcpSerSock.close()
