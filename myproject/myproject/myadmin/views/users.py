from django.shortcuts import render
from django.http import HttpResponse
from datetime import datetime

from django.core.paginator import Paginator # 分页
from django.db.models import Q # 查询

from common.models import Users

# =================会员信息管理===================
#浏览会员信息
def index(request,pIndex):
	'''浏览信息'''
	list = Users.objects.all() # 获取全部信息
	#context = {"userlist":list} # 使用变量接收

	#获取会员信息查询对象
	mod = Users.objects
	mywhere = [] #定义一个用于存放搜索条件列表

	#获取、判断并封装关于keyword键搜索
	kw = request.GET.get("username",None)
	if kw :
		#查询账号或姓名中含有关键字的
		list = mod.filter(username__contains=kw) or mod.filter(name__contains=kw)
		mywhere.append("keyword="+kw)
	else:
		list = mod.filter()

	#获取、判断并封装会员sex属性搜索条件
	sex = request.GET.get('sex','')
	if sex != '':
		list = mod.filter(sex=sex)
		mywhere.append('sex='+sex)

	#分页
	pIndex=int(pIndex)
	p = Paginator(list,4)
	#防止越界
	maxpages = p.num_pages # 最大页数
	if pIndex > maxpages:
		pIndex = maxpages
	if pIndex < 1:
		pIndex = 1
	"""if pIndex == "":
		pIndex = 1"""
	list2 = p.page(pIndex) # 当前页
	plist =p.page_range # 页码
	#封装信息输出
	context = {"userlist":list2,"plist":plist,"pIndex":int(pIndex),"maxpages":maxpages,"mywhere":mywhere}
	return render(request,"myadmin/users/index.html",context)

def add(request):
	'''加载添加信息'''
	return render(request,"myadmin/users/add.html")

def insert(request):
	'''执行添加'''
	try:
		ob = Users() #实例化
		ob.username = request.POST['username']
		ob.name = request.POST['name']
		# 获取密码并md5
		import hashlib
		m = hashlib.md5()
		m.update(bytes(request.POST['password'], encoding="utf8"))
		ob.password = m.hexdigest() #md5加密格式
		ob.sex = request.POST['sex']
		ob.address = request.POST['address']
		ob.code = request.POST['code']
		ob.phone = request.POST['phone']
		ob.email = request.POST['email']
		ob.state = 1 # 指定状态
		ob.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S") # 使用now方法
		ob.save() # 保存数据
		context = {"info": "添加成功！"}
	except Exception as err:
		print(err)
		context = {"info":"添加失败！"}
	return render(request,"myadmin/info.html",context)

def delete(request,uid):
	'''删除信息'''
	try:
		ob = Users.objects.get(id=uid) # ob获取对应id信息
		ob.delete() # 删除
		context = {"info": "删除成功！"}
	except Exception as err:
		print(err)
		context = {"info":"删除失败！"}
	return render(request,"myadmin/info.html",context)

def edit(request,uid):
	'''加载编辑信息页面'''
	try:
		ob = Users.objects.get(id=uid)  # ob获取对应id信息
		context = {"user": ob} #用变量接收获取的信息
		return render(request, "myadmin/users/edit.html", context)
	except Exception as err:
		context = {"info": "没有找到要修改的信息！"}
		return render(request, "myadmin/info.html", context)

def update(request,uid):
	'''执行编辑信息'''
	try:
		ob = Users.objects.get(id=uid) # 获取对象
		ob.name = request.POST['name']
		ob.sex = request.POST['sex']
		ob.address = request.POST['address']
		ob.code = request.POST['code']
		ob.phone = request.POST['phone']
		ob.email = request.POST['email']
		ob.state = request.POST['state'] #默认会给状态
		ob.save() # 保存数据
		context = {"info": "修改成功！"}
	except Exception as err:
		print(err)
		context = {"info":"修改失败！"}
	return render(request,"myadmin/info.html",context)

def reset(request,uid):
	'''加载重置密码页面'''
	try:
		ob = Users.objects.get(id=uid)  # ob获取对应id信息
		context = {"user": ob} #用变量接收获取的信息
		return render(request, "myadmin/users/reset.html", context)
	except Exception as err:
		context = {"info": "没有找到要修改的信息！"}
		return render(request, "myadmin/info.html", context)

def pwd(request,uid):
	'''执行重置密码信息'''
	try:
		ob = Users.objects.get(id=uid) # 获取对象
		m1 = request.POST['password']
		m2 = request.POST['password']
		if m1 != m2 :
			context1 = {"info":"两次密码输入不相同！"}
			return render(request,"myadmin/info.html",context1)
		# 获取密码并md5
		import hashlib
		m1 = hashlib.md5()
		m1.update(bytes(request.POST['password'], encoding="utf8"))
		ob.password = m1.hexdigest()
		ob.save() # 保存数据
		context = {"info": "重置成功！"}
	except Exception as err:
		print(err)
		context = {"info":"重置失败！"}
	return render(request,"myadmin/info.html",context)