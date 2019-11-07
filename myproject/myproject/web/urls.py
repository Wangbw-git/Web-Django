from django.urls import path,re_path

from web.views import index,cart,orders,vip

urlpatterns = [
    # 前台首页
    path('', index.index, name="index"),	#商城首页
    path('list', index.lists, name="list"),# 商品列表
    re_path(r'^list/(?P<pIndex>[0-9]+)$',index.lists,name="list"), # 分页商品列表展示
    re_path(r'^detail/(?P<gid>[0-9]+)$', index.detail, name="detail"),#商品详情 # 这里处理正则需要导入re_path

	# 会员及个人中心等路由配置
    path('login',index.login,name="login"),
    path('dologin',index.dologin,name="dologin"),
    path('logout',index.logout,name="logout"),

	# 注册会员
    path('register', index.register ,name="register"), # 注册页面
    path('doregister',index.doregister,name="doregister"), # 实现注册功能
    path('verify',index.verify,name="web_verify"),

    # 购物车路由
    path('cart', cart.index,name='cart_index'), #浏览购物车
    path('cart/add/(?P<gid>[0-9]+)', cart.add,name='cart_add'), #添加购物车
    path('cart/del/(?P<gid>[0-9]+)', cart.delete,name='cart_del'), #从购物车中删除一个商品
    path('cart/clear', cart.clear,name='cart_clear'), #清空购物车
    path('cart/change', cart.change,name='cart_change'), #更改购物车中商品数量

    # 订单处理
    path('orders/add', orders.add,name='orders_add'), # 订单的表单页
    path('orders/confirm', orders.confirm,name='orders_confirm'), # 订单确认页
    path('orders/insert', orders.insert,name='orders_insert'), # 执行订单添加操作

    # 会员中心
    path('vip/orders',vip.viporders,name='vip_orders'), # 会员中心我的订单
    path('vip/orders/(?P<pIndex>[0-9]+)',vip.viporders,name='vip_orders'), # 分页
    path('vip/odstate',vip.odstate,name='vip_odstate'), # 修改订单状态（确认收货）
    path('vip/info', vip.info,name='vip_info'), #会员中心的个人信息
    path('vip/update', vip.update,name='vip_update'), #执行修改会员信息
    path('vip/resetps', vip.resetps,name='vip_resetps'), #重置密码表单
    path('vip/doresetps', vip.doresetps,name='vip_doresetps'), #执行重置密码
]
