from django.shortcuts import render
from django.http import HttpResponse
from django.db.models import Q
from django.core.paginator import Paginator

from common.models import Goods,Users,Orders,Detail

# Create your views here.
def index(request,pIndex=1):
	'''浏览信息'''
	# 获取订单信息
	mod = Orders.objects
	mywhere = []

	# 获取、判断并封装关于keyword键的搜索
	kw = request.GET.get("keyword",None)
	if kw:
		# 查询收件人和地址中只要含有关键字的都可以
		list = mod.filter(Q(linkman__contains=kw)|Q(address__contains=kw))
		mywhere.append("keyword="+kw)
	else:
		list = mod.filter()

	# 获取、判断并封装订单状态state搜索条件
	state = request.GET.get('state','')
	if state != '':
		list = list.filter(state=state)
		mywhere.append("state="+state)


	# 分页处理
	pIndex = int(pIndex)
	page = Paginator(list,5)
	maxpages = page.num_pages
	# 判断是否越界
	if pIndex > maxpages:
		pIndex=maxpages
	if pIndex < 1:
		pIndex = 1
	list2 = page.page(pIndex)# 当前页数据
	plist =page.page_range # 页码数列表


	#遍历订单信息并追加 下订单人姓名信息
	for od in list2:
		user = Users.objects.only('name').get(id=od.uid)
		od.name = user.name

	context = {"orderslist":list2,'plist':plist,'pIndex':pIndex,'maxpages':maxpages,'mywhere':mywhere}
	return render(request,"myadmin/orders/index.html",context)

def detail(request,oid):
	'''订单详情'''
	try:
		# 加载订单信息
		orders = Orders.objects.get(id=oid)
		if orders != None:
			user = Users.objects.only('name').get(id=orders.uid)
			orders.name = user.name

		# 加载订单详情
		dlist = Detail.objects.filter(orderid=oid)
		# 查看详情，获取相应图片信息
		for og in dlist:
			og.picname = Goods.objects.only('picname').get(id=og.goodsid).picname

		# 放置模板变量，加载模板并输出
		context = {'orders':orders,'detaillist':dlist}
		return render(request,"myadmin/orders/detail.html",context)
	except Exception as err:
		print(err)
		context = {'info': '没有找到要查看的信息！'}
	return render(request, "myadmin/info.html", context)

def state(request):
	'''订单状态'''
	try:
		oid = request.GET.get('oid','0')
		ob = Orders.objects.get(id=oid)
		ob.state = request.GET['state']
		ob.save()
		context = {'info':'修改成功！'}
	except Exception as err:
		print(err)
		context = {'info': '修改失败！'}
	return render(request, "myadmin/info.html", context)