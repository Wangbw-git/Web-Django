from django.urls import path
from myadmin.views import index,users,type,goods,orders # 导入users

urlpatterns = [
    #后台首页
    path('', index.index, name="myadmin_index"),

    # 后台管理员路由
    path('login', index.login, name="myadmin_login"),
    path('dologin', index.dologin, name="myadmin_dologin"),
    path('logout', index.logout, name="myadmin_logout"),
    path('verify', index.verify, name="myadmin_verify"), #验证码

    #会员信息管理路由
    path('users/(?P<pIndex>[0-9]+)', users.index, name="myadmin_users_index"),
    path('users/add', users.add, name="myadmin_users_add"), # 建各路由
    path('users/insert', users.insert, name="myadmin_users_insert"),
    path('users/del/(?P<uid>[0-9]+)', users.delete, name="myadmin_users_del"), # 由于内含del方法，所以这里使用delete
    path('users/edit/(?P<uid>[0-9]+)', users.edit, name="myadmin_users_edit"), # 导入正则
    path('users/update/(?P<uid>[0-9]+)', users.update, name="myadmin_users_update"),
    path('users/reset/(?P<uid>[0-9]+)', users.reset, name="myadmin_users_reset"), #重置
    path('users/pwd/(?P<uid>[0-9]+)', users.pwd, name="myadmin_users_pwd"), #重置

    #商品类别信息管理路由
    path('type', type.index, name="myadmin_type_index"),
    path('type/add/(?P<tid>[0-9]+)', type.add, name="myadmin_type_add"), # 建各路由
    path('type/insert', type.insert, name="myadmin_type_insert"),
    path('type/del/(?P<tid>[0-9]+)', type.delete, name="myadmin_type_del"), # 由于内含del方法，所以这里使用delete
    path('type/edit/(?P<tid>[0-9]+)', type.edit, name="myadmin_type_edit"), # 导入正则
    path('type/update/(?P<tid>[0-9]+)', type.update, name="myadmin_type_update"),

	# 后台商品信息管理
	path('goods/(?P<pIndex>[0-9]+)', goods.index, name="myadmin_goods_index"),
	path('goods/add', goods.add, name="myadmin_goods_add"),
	path('goods/insert', goods.insert, name="myadmin_goods_insert"),
	path('goods/del/(?P<gid>[0-9]+)', goods.delete, name="myadmin_goods_del"),
	path('goods/edit/(?P<gid>[0-9]+)', goods.edit, name="myadmin_goods_edit"),
	path('goods/update/(?P<gid>[0-9]+)', goods.update, name="myadmin_goods_update"),

	# 订单信息管理路由
	path('orders',orders.index,name="myadmin_orders_index"),
	path('orders/(?P<pIndex>[0-9]+)',orders.index,name="myadmin_orders_index"),
	path('orders/detail/(?P<oid>[0-9]+)',orders.detail,name="myadmin_orders_detail"),
	path('orders/state',orders.state,name="myadmin_orders_state"),
]
