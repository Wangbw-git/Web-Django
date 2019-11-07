from django.shortcuts import render
from django.http import HttpResponse

from common.models import Types
# Create your views here.
def index(request):
	'''浏览信息'''
	#list = Types.objects.all() # 获取全部信息
	list = Types.objects.extra(select={'_has': 'concat(path,id)'}).order_by('_has') # 指定一个字段 选取的是名为_has的path,id的字段，并根据该字段进行排序
	#遍历查询结果，添加一个类别缩进效果属性
	for ob in list:
		ob.pname = '. . . . '*(ob.path.count(',')-1)
	context = {"typeslist":list} # 使用变量接收
	return render(request,"myadmin/type/index.html",context)

def add(request,tid):
	'''加载添加信息'''
	#获取父类别信息
	if tid == '0':
		context = {'pid':0,'path':'0,','name':'根类别'}
	else:
		ob = Types.objects.get(id=tid)
		context = {'pid':ob.id,'path':ob.path+str(ob.id)+',','name':ob.name} # 这里需要将ob.id强转字符串类型
	return render(request,"myadmin/type/add.html",context)

def insert(request):
	'''执行添加'''
	try:
		ob = Types() #实例化
		ob.name = request.POST['name']
		ob.pid = request.POST['pid']
		ob.path = request.POST['path']
		ob.save() # 保存数据
		context = {"info": "添加成功！"}
	except Exception as err:
		print(err)
		context = {"info":"添加失败！"}
	return render(request,"myadmin/info.html",context)

def delete(request,tid):
	'''删除信息'''
	try:
		ob = Types.objects.get(id=tid) # ob获取对应id信息
		count = Types.objects.filter(pid=tid).count() # 获取父类别为选定类别id的数量
		if count > 0:
			context1 = {"info":"该分类下存在子分类，无法删除！"}
			return render(request,"myadmin/info.html",context1)
		ob.delete() # 删除
		context = {"info": "删除成功！"}
	except Exception as err:
		print(err)
		context = {"info":"删除失败！"}
	return render(request,"myadmin/info.html",context)

def edit(request,tid):
	'''加载编辑信息页面'''
	try:
		ob = Types.objects.get(id=tid)  # ob获取对应id信息
		context = {"type": ob} #用变量接收获取的信息
		return render(request, "myadmin/type/edit.html", context)
	except Exception as err:
		context = {"info": "没有找到要修改的信息！"}
		return render(request, "myadmin/info.html", context)

def update(request,tid):
	'''执行编辑信息'''
	try:
		ob = Types.objects.get(id=tid) # 获取对象
		ob.name = request.POST['name']
		ob.save() # 保存数据
		context = {"info": "修改成功！"}
	except Exception as err:
		print(err)
		context = {"info":"修改失败！"}
	return render(request,"myadmin/info.html",context)