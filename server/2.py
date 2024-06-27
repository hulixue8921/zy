import json
import socket

x = {"model": "app", "api": "appAction"}
x['username'] = "test4"
x['passwd'] = "123456"
x['token']='eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJkYXRhIjp7InJpZ2h0IjpbImFkbWluIiwiYXBwOjpjbXMiXSwidXNlcm5hbWUiOiJyb290IiwicGFzc3dkIjoiMTIzNDU2Iiwicm9sZUlkIjoyfSwiZXhwIjoxNjk1NzE2MjUzLjEwODk2NTksImlzcyI6Imx5cnJhIn0.48F85yzy9OLO9oirnUH5fE3Brh3P4Kp9ewk_P9UYom4'
x['fabuId'] = 69
x['type'] ="start"
x['roleName'] = 't1'
x['memName'] = '发布系统:正式环境'
x['rightIds'] = {'1': 1}
x['userId'] = '2'
s = socket.socket()
s.connect(("localhost", 8888))
d = json.dumps(x) + "\n"
s.send(d.encode('utf-8'))

z = s.recv(1024)
print(z)

"""
h=json.loads(z)
print(h['mem'])
"""
