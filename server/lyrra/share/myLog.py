import logging
import configparser

globalDict = {}


def wapper(cls):
    def A(*args, **kwargs):
        if cls not in globalDict:
            globalDict[cls] = cls(*args, **kwargs)
        return globalDict[cls]

    return A


@wapper
class MyLog:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./etc/config.ini')

        _dict = {}
        _dict['info'] = logging.INFO
        _dict['debug'] = logging.DEBUG
        _dict['error'] = logging.ERROR
        _dict['warn'] = logging.WARN
        _dict['critical'] = logging.CRITICAL

        logger = logging.getLogger()
        self.logger = logger
        logger.setLevel(_dict[config['log']['level']])

        logger.propagate = False
        formatter = logging.Formatter(u"%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s")

        filter1 = logging.Filter()
        filter1.filter = lambda x: x.levelno == logging.DEBUG
        hander1 = logging.FileHandler('./logs/debug')
        hander1.setFormatter(formatter)
        hander1.addFilter(filter1)

        filter2 = logging.Filter()
        filter2.filter = lambda x: x.levelno == logging.INFO
        hander2 = logging.FileHandler('./logs/info')
        hander2.setFormatter(formatter)
        hander2.addFilter(filter2)

        filter3 = logging.Filter()
        filter3.filter = lambda x: x.levelno == logging.WARN
        hander3 = logging.FileHandler('./logs/warn')
        hander3.setFormatter(formatter)
        hander3.addFilter(filter3)

        filter4 = logging.Filter()
        filter4.filter = lambda x: x.levelno == logging.ERROR
        hander4 = logging.FileHandler('./logs/error')
        hander4.setFormatter(formatter)
        hander4.addFilter(filter4)

        filter5 = logging.Filter()
        filter5.filter = lambda x: x.levelno == logging.CRITICAL
        hander5 = logging.FileHandler('./logs/critical')
        hander5.setFormatter(formatter)
        hander5.addFilter(filter5)

        logger.addHandler(hander1)
        logger.addHandler(hander2)
        logger.addHandler(hander3)
        logger.addHandler(hander4)
        logger.addHandler(hander5)
