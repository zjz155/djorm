from django.db import models

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String
from sqlalchemy import create_engine

from sqlalchemy import event
from sqlalchemy import exc
import os

# from djorm.settings import  engine

# 使用多进程连接池
# 创建连接引擎
engine = create_engine("mysql+pymysql://root:123456@localhost:3306/cloudDB", pool_size=25, max_overflow=0)

@event.listens_for(engine, "connect")
def connect(dbapi_connection, connection_record):
    connection_record.info['pid'] = os.getpid()    

@event.listens_for(engine, "checkout")
def checkout(dbapi_connection, connection_record, connection_proxy):
    pid = os.getpid()
    if connection_record.info['pid'] != pid:
        connection_record.connection = connection_proxy.connection = None
        raise exc.DisconnectionError(
                "Connection record belongs to pid %s, "
                "attempting to check out in pid %s" %
                (connection_record.info['pid'], pid)
        )    

# ----- 以上带码可置于settings中, 各应用通过导入包获得数据库连接引擎engine-------

# Create your models here.

# 创建数据库表基类
Base = declarative_base()

class Account(Base):
    __tablename__ = "account"
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(10))
    password = Column(String(255))

    def __repr__(self):
        obj = "<object:(%s, %s)>" % (self.id, self.username)
        return obj

# 创建数据库表结构
Base.metadata.create_all(engine)