from lyrra.share.myLog import MyLog
import json


class MyException(Exception):
    exceptData = {
        '404': {
            'code': 404,
            'message': "数据格式不对"
        },
        '403': {
            'code': 403,
            'message': "权限不够"
        },
        '400': {
            'code': 400,
            'message': "用户已存在"
        },
        '401': {
            'code': 401,
            'message': "账号名或密码不正确"
        },
        '402': {
            'code': 402,
            'message': "token问题或过期"
        },
        '500': {
            'code': 500,
            'message': '内部错误'
        },
        '405':{
            'code': 405,
            'message': "此接口不能并发执行，请稍等"
        }
    }

    def __init__(self, *args, **kwargs):
        self._log = MyLog().logger
        self._socket = kwargs['socket']

    def logError(self, args):
        self._log.error(args)

    def reply(self, args):
        self._socket.write(json.dumps(MyException.exceptData[args]).encode('utf-8'))
