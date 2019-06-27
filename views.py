from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.views import View

from sqlalchemy.orm import sessionmaker

from mysqlapp.models import Account, engine


# from djorm.settings import  engine


# Create your views here.
class RegisterView(View):
    def get(self, request,username, password, *args, **kwargs):
        # 连接数据库
        DBSession = sessionmaker(bind=engine)
        # 创建session对象
        session = DBSession()
        # 创建新account对象
        account = Account(username=username, password=password)

        session.add(account)

        # 提交保存到数据库
        session.commit()

        account_list = session.query(Account).all()        
        users_account_info = [{"username": obj.username, "password": obj.password} for obj in account_list ]
        
        dic = {
            "users_account_info": users_account_info,
        }

        # 关闭session
        session.close()

        return JsonResponse(dic)