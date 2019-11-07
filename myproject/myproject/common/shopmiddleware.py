from django.shortcuts import render
from django.http import HttpResponse

import re # 导入正则

from django.shortcuts import redirect # 导入重定向
from django.urls import reverse # 导入解析

class ShopMiddleware():
    def __init__(self, get_response):
        self.get_response = get_response
        print("ShopMiddleware")
        # One-time configuration and initialization.


    def __call__(self, request):
        # 定义网站后台不用登录也可访问的路由url
        urllist = ['/myadmin/login', '/myadmin/dologin', '/myadmin/logout','/myadmin/verify'] #添加验证码
        # 获取当前请求路径
        path = request.path
        # print("Hello World!"+path)
        # 判断当前请求是否是访问网站后台,并且path不在urllist中
        if re.match("/myadmin", path) and (path not in urllist):
            # 判断当前用户是否没有登录
            if "adminuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('myadmin_login'))

        # 网站前台会员登录判断
        if re.match("^/orders", path) or re.match("^/vip", path):
            # 判断当前会员是否没有登录
            if "vipuser" not in request.session:
                # 执行登录界面跳转
                return redirect(reverse('login'))

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response