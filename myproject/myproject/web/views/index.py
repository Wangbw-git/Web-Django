from django.shortcuts import render
from django.http import HttpResponse

from django.shortcuts import redirect
from django.urls import reverse # 导入重定向

from common.models import Users,Types,Goods
from datetime import datetime
from django.core.paginator import Paginator
import random
from django.views.decorators.http import require_POST # 导入只POST方式的装饰器
from ..forms import RegisterForm
import hashlib

# 编辑公共信息加载函数
def loadinfo(request):
	lists = Types.objects.filter(pid=0)
	context = {"typelist":lists}
	return context

# =============商品展示========================
def index(request):
    '''项目前台首页'''
    context = loadinfo(request)

    return render(request,"web/index.html",context)

def lists(request,pIndex=1):
    '''商品列表页'''
    context = loadinfo(request)
	# 商品列表展示
    mod = Goods.objects
    mywhere = [] #跳转存放列表
	#判断封装搜索条件
    tid = int(request.GET.get('tid',0))
    if tid > 0:
        list = mod.filter(typeid__in=Types.objects.only('id').filter(pid=tid))
        mywhere.append("tid="+str(tid)) #添加一个商品跳转
    else:
        list = mod.filter()
    # 执行分页处理
    pIndex = int(pIndex)
    page = Paginator(list, 8)  # 以5条每页创建分页对象
    maxpages = page.num_pages  # 最大页数
    # 判断页数是否越界
    if pIndex > maxpages:
        pIndex = maxpages
    if pIndex < 1:
        pIndex = 1
    list2 = page.page(pIndex)  # 当前页数据
    plist = page.page_range  # 页码数列表

    context['goodslist'] = list2
    context['plist'] = plist
    context['pIndex'] = pIndex
    context['mywhere'] = mywhere
    return render(request,"web/list.html",context)

def detail(request,gid):
    '''商品详情页'''
    context = loadinfo(request)
    ob = Goods.objects.get(id=gid)
    ob.clicknum += 1 # 点击量逐次加1
    ob.save()
    context['goods'] = ob
    return render(request,"web/detail.html",context)

# ==============前台会员登录====================
def login(request):
	'''会员登录表单'''
	return render(request,"web/login.html")

def dologin(request):
	'''会员执行登录'''
	# 校验验证码
	verifycode = request.session['verifycode']
	code = request.POST['code']
	if verifycode != code:
		context = {"info":"验证码输入错误！"}
		return render(request,"web/login.html",context)

	try:
		# 根据账号获得登录信息
		user = Users.objects.get(username=request.POST['username'])
		#根据用户状态判断是否合法
		if user.state == 0 or user.state == 1:
			#验证密码
			import hashlib
			m = hashlib.md5()
			m.update(bytes(request.POST['password'],encoding="utf8"))
			if user.password == m.hexdigest():
				# 密码验证成功后，将其储存在session中
				request.session['vipuser'] = user.toDict()
				return redirect(reverse('index'))
			else:
				context = {"info":"密码输入错误！"}
		else:
			context = {"info":"此用户为非法用户！"}
	except:
		context = {"info":"登录账号错误！"}
	return render(request,"web/login.html",context)

def logout(request):
	'''会员退出'''
	#清除登录界面信息
	del request.session['vipuser']
	#跳出登录界面（url地址改变）
	return redirect(reverse('login'))

def register(request):
	'''跳转注册页面'''
	return render(request,"web/register.html")

# def doregister(request):
# 	'''执行注册'''
# 	try:
# 		# 判断账号有无重名
# 		ob = Users.objects.all()
# 		for old in ob:
# 			if old.username == request.POST['username']:
# 				context = {"info":"账户名已存在！"}
# 				return render(request,"web/register.html",context)
# 		# 判断密码是否一致
# 		if request.POST['password'] != request.POST['repassword']:
# 			context = {"info":"两次输入的密码不一致！"}
# 			return render(request,"web/register.html",context)
# 		# 获取输入的信息
# 		new = Users()
# 		new.username = request.POST['username']
# 		new.sex = request.POST['sex']
# 		new.name = request.POST['name']
# 		new.addtime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
# 		new.state = 1
# 		# 对密码进行MD5加密
# 		import hashlib
# 		m = hashlib.md5()
# 		m.update(bytes(request.POST['password'],encoding="utf8"))
# 		new.password = m.hexdigest()
# 		#保存
# 		new.save()
#
# 		request.session['vipuser'] = new.toDict()
# 		return redirect(reverse('index'))
# 	except Exception as err:
# 		print(err)
# 		context = {"info":"注册失败！"}
# 	return render(request,"myadmin/info.html",context)

@require_POST # 载入装饰器
def doregister(request):
	'''注册'''
	form = RegisterForm(request.POST)
	# 如果is_valid返回True，那么说明验证成功
	if form.is_valid():
		username = form.cleaned_data.get('username')
		name = form.cleaned_data.get('name')
		password = form.cleaned_data.get('password')
		sex = form.cleaned_data.get('sex')
		# md5的参数只能是bytes类型，所以需要把password(str类型)转换成bytes类型
		# str --> bytes=encode
		md5_password = hashlib.md5(password.encode('utf8')).hexdigest() #转换成md5类型
		Users.objects.create(username=username,name=name,password=md5_password,sex=sex) # 创建一条数据
		return redirect('/') # 返回根目录
	else:
		# 否则代表验证失败，也就是说数据传过来有问题
		context = {"info":"注册失败！"}
		return render(request,"web/register.html",context)


def verify(request):
	'''验证码'''
	import random
	from PIL import Image, ImageDraw, ImageFont
	# 定义变量，用于画面的背景色、宽、高
	bgcolor = (random.randrange(20, 100), random.randrange(20, 100), 100)
	# bgcolor = (242,164,247) #固定验证码背景颜色
	size = width, height = 100, 40

	# 创建画面对象
	im = Image.new('RGB', size, bgcolor)
	# 创建画笔对象
	draw = ImageDraw.Draw(im)
	# 调用画笔的point()函数绘制噪点
	for i in range(0, 100):
		xy = (random.randrange(0, width), random.randrange(0, height))  # 随机一个噪点位置
		fill = (random.randrange(0, 255), 255, random.randrange(0, 255))  # 随机一个噪点颜色
		draw.point(xy, fill=fill)

	# 定义验证码的备选值
	# str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
	str2 = '0123456789'
	# 随机选取4个值作为验证码
	rand_str = ''
	for i in range(0, 4):
		rand_str += str2[random.randrange(0, len(str2))]

	# 构造字体对象
	font = ImageFont.truetype('static/myadmin/fonts/Ubuntu/Ubuntu-Bold.TTF', 23)
	# font = ImageFont.truetype().font #采用默认字体
	# 构造字体颜色
	fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))

	# 绘制4个字
	draw.text((10, 2), rand_str[0], font=font, fill=fontcolor)
	draw.text((30, 6), rand_str[1], font=font, fill=fontcolor)
	draw.text((55, 2), rand_str[2], font=font, fill=fontcolor)
	draw.text((80, 6), rand_str[3], font=font, fill=fontcolor)

	# 释放画笔
	del draw
	# 存入session,用于做进一步的验证
	request.session['verifycode'] = rand_str
	# 内存文件操作
	import io
	buf = io.BytesIO()

	# 将图片存在内存里，文件类型为PNG
	im.save(buf, 'png')
	# 将内存中的图片数据返回到客户端，MIME类型为图片png
	return HttpResponse(buf.getvalue(), 'Image/png')