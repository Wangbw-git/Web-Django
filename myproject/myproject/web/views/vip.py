from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse # 导入重定向

from common.models import Users,Types,Goods,Orders,Detail
from django.core.paginator import Paginator

# 编辑公共信息加载函数
def loadinfo(request):
    lists = Types.objects.filter(pid=0)
    context = {"typelist":lists}
    return context

# ===========================订单详情===========================
def viporders(request,pIndex=1):
    '''浏览订单信息'''
    context = loadinfo(request)
    mywhere = []
    # 获取当前登录者的订单信息
    odlist = Orders.objects.filter(uid=request.session['vipuser']['id'])

    # 获取、判断并封装订单状态state搜索条件
    state = request.GET.get('state', '')
    if state != '':
        odlist = odlist.filter(state=state)
        mywhere.append("state=" + state)

    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(odlist, 2)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    odlist2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    # 遍历订单信息，查询对应的详情信息
    for od in odlist2:
        delist = Detail.objects.filter(orderid=od.id)
        # 遍历订单详情，获取图片信息
        for og in delist:
            og.picname = Goods.objects.only("picname").get(id = og.goodsid).picname
        od.detaillist = delist

    # 将整理好的订单信息放置到模板遍历中
    context['orderslist'] = odlist2
    context['plist'] = plist
    context['mywhere'] = mywhere
    context['pIndex'] = pIndex
    return render(request,"web/viporders.html",context)

def odstate(request):
    '''修改订单状态'''
    try:
        oid = request.GET.get("oid",0)
        ob = Orders.objects.get(id=oid)
        ob.state = request.GET['state']
        ob.save()
        return redirect(reverse('vip_orders'))
    except Exception as err:
        print(err)
        return HttpResponse("订单处理失败！")

# =======================个人中心===========================
def info(request):
    '''个人信息浏览'''
    ob = Users.objects.filter(id=request.session['vipuser']['id'])[0]
    print(ob)
    context = {"vip":ob}
    return render(request,"web/vipinfo.html",context)

def update(request):
    '''个人信息更改'''
    try:
        ob = Users.objects.filter(id=request.session['vipuser']['id'])[0]
        ob.name = request.POST['name']
        ob.sex = request.POST['sex']
        ob.address = request.POST['address']
        ob.code = request.POST['code']
        ob.phone = request.POST['phone']
        ob.email = request.POST['email']
        ob.save()
        return render(request,"web/vipinfoconfirm.html")
    except Exception as err:
        print(err)
    return redirect(reverse('vip_info'))

def resetps(request):
    '''重置密码'''
    try:
        ob = Users.objects.filter(id=request.session['vipuser']['id'])[0]
        context = {"vip": ob}  # 用变量接收获取的信息
        return render(request, "web/vipresetps.html", context)
    except Exception as err:
        print(err)
        context = {"info": "没有找到要修改的信息！"}
        return render(request, "web/vipinfo.html", context)

def doresetps(request):
    '''执行重置密码'''
    try:
        ob = Users.objects.filter(id=request.session['vipuser']['id'])[0]
        m1 = request.POST['password']
        m2 = request.POST['password']
        if m1 != m2:
            context1 = {"info": "两次密码输入不相同！"}
            return render(request, "web/vipinfoconfirm.html", context1)
        # 获取密码并md5
        import hashlib
        m1 = hashlib.md5()
        m1.update(bytes(request.POST['password'], encoding="utf8"))
        ob.password = m1.hexdigest()
        ob.save()  # 保存数据
        context = {"info": "重置成功！"}
    except Exception as err:
        print(err)
        context = {"info": "重置失败！"}
    return render(request, "web/vipinfoconfirm.html", context)