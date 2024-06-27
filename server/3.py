import json
import socket

x = {"model": "user", "api": "load", "username": "root", "passwd": "123456"}
s = socket.socket()
s.connect(("localhost", 8888))
d = json.dumps(x) + "\n"
s.send(d.encode('utf-8'))

z = s.recv(1024)

h=json.loads(z)
#print(h['token'])
print(h)
