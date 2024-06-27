import sqlalchemy as sa
import configparser
from sqlalchemy import func


class MyTable:
    def __init__(self):
        config = configparser.ConfigParser()
        config.read('./etc/config.ini')
        self.user = config['mysql']['user']
        self.passwd = config['mysql']['passwd']
        self.db = config['mysql']['db']
        self.ip = config['mysql']['ip']
        self.port = config['mysql']['port']
        self.min = int(config['mysql']['min'])
        self.max = int(config['mysql']['max'])

        metadata = sa.MetaData()
        self.metadata = metadata
        self.t_user = sa.Table(
            "t_user",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("username", sa.String(64), unique=True),
            sa.Column("passwd", sa.String(64)),
            sa.Column("roleId", sa.Integer, server_default='0')
        )
        self.t_role = sa.Table(
            "t_role",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column('name', sa.String(64), unique=True)
        )
        self.t_mem = sa.Table(
            "t_mem",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("value", sa.String(255), unique=True)
        )
        self.t_role_mem = sa.Table(
            "t_role_mem",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("roleId", sa.Integer),
            sa.Column("memId", sa.Integer)
        )
        self.t_right = sa.Table(
            "t_right",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("value", sa.String(255), unique=True),
            sa.Column("name", sa.String(255))
        )
        self.t_role_right = sa.Table(
            "t_role_right",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("roleId", sa.Integer),
            sa.Column("rightId", sa.Integer)
        )
        self.t_app = sa.Table(
            "t_app",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("name", sa.String(255), unique=True),
            sa.Column("project", sa.String(255)),
            sa.Column("git", sa.String(255)),
        )
        self.t_role_fabu = sa.Table(
            "t_role_fabu",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("roleId", sa.Integer),
            sa.Column("fabuId", sa.Integer)
        )
        self.t_env = sa.Table(
            "t_env",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("name", sa.String(255), unique=True)
        )
        self.t_fabu = sa.Table(
            "t_fabu",
            metadata,
            sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
            sa.Column("appId", sa.Integer),
            sa.Column("envId", sa.Integer),
            sa.Column("commit", sa.String(255), server_default="noCommit")
        )

    def createTable(self):
        engine = sa.create_engine(
            'mysql+pymysql://%s:%s@%s:%s/%s' % (self.user, self.passwd, self.ip, self.port, self.db))
        self.metadata.create_all(engine)
