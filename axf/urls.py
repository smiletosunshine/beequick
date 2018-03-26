
from django.conf.urls import url

from . import views

urlpatterns = [
    #home
    url(r'^home/$', views.home),
    #market
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market),

    #修改购物车
    url(r'^changeCart/(\w+)/$', views.changeCart),

    #cart
    url(r'^cart/$', views.cart),
    #下单
    url(r'^downorder/$', views.downorder),



    #mine
    url(r'^mine/$', views.mine),
    #注册
    url(r'^regist/$', views.regist),
    #退出登陆
    url(r'^quit/$', views.quit),
    #登陆
    url(r'^loginaxf/$', views.loginaxf),

]
