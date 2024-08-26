import socket
import configparser
import json
import sys
import os


class MySocket(socket.socket):
    def __init__(self):
        super().__init__()
        config = configparser.ConfigParser()
        '''
        解决 打包 读取配置文件问题
        '''
        basedir = os.path.dirname(__file__)
        paths=basedir.split("lyrra")
        path=paths[0]+"etc/config.ini"
        # config.read(sys.path[0]+'/etc/config.ini')
        config.read(path)
        self.ip = config['server']['ip']
        self.port = int(config['server']['port'])
        self.connect((self.ip, self.port))

    def send(self, data):
        sentData = json.dumps(data) + '\n'
        super().send(sentData.encode('utf-8'))
        getData = b''
        while True:
            chunk=self.recv(1024)
            if not chunk:
                break
            getData += chunk
        getData = json.loads(getData)
        return getData
