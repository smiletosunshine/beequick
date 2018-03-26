from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
# Create your views here.
from .models import Wheel, Nav, Mustbuy, Shop, MainShow, FoodTypes, Goods, User, Cart, Order

import random,time


def home(request):
    swiperlist = Wheel.objects.all()
    navlist = Nav.objects.all()
    mustbuylist = Mustbuy.objects.all()
    shoplist = Shop.objects.all()
    shoplist1 = shoplist[0]
    shoplist2 = shoplist[1:3]
    shoplist3 = shoplist[3:7]
    shoplist4 = shoplist[7:11]
    mainshowlist = MainShow.objects.all()
    return render(request, "axf/home/home.html", {"swiperlist":swiperlist,"navlist":navlist,"mustbuylist":mustbuylist,"shoplist1":shoplist1,"shoplist2":shoplist2,"shoplist3":shoplist3,"shoplist4":shoplist4,"mainshowlist":mainshowlist})




def market(request, gid, cid, sortflag):
    #左侧分组信息列表
    leftmenu = FoodTypes.objects.all()

    #展示组的商品列表
    productlist = Goods.objects.filter(categoryid=gid)
    if cid != "0":
        productlist = productlist.filter(childcid=cid)
    #排序
    if sortflag == "1":
        productlist = productlist.order_by("productnum")
    elif sortflag == "2":
        productlist = productlist.order_by("price")
    elif sortflag == "3":
        productlist = productlist.order_by("-price")

    #获取子组
    childlist = []
    foodtypeinfo = leftmenu.get(typeid=gid)
    # "103532","优选水果","全部分类:0#进口水果:103534#国产水果:103533",3
    childstr = foodtypeinfo.childtypenames
    #全部分类:0#进口水果:103534#国产水果:103533
    arr = childstr.split("#")
    for partstr in arr:
        #进口水果:103534
        partarr = partstr.split(":")
        obj = {"name":partarr[0], "cid":partarr[1]}
        childlist.append(obj)


    # 商品初始数量
    token = request.COOKIES.get("token")
    carts = Cart.objects.filter(user__userToken=token)
    for cart in carts:
        for good in productlist:
            if cart.product.productid == good.productid:
                good.num = cart.productNum


    return render(request, "axf/market/market.html", {"leftmenu":leftmenu,"productlist":productlist,"childlist":childlist,"gid":gid,"cid":cid,"carts":carts})





def cart(request):
    carts = Cart.objects.filter(user__userToken=request.COOKIES.get("token"))
    return render(request, "axf/cart/cart.html", {"carts":carts})



def mine(request):
    sk = request.COOKIES.get("name")
    username = request.session.get(sk)
    return render(request, "axf/mine/mine.html", {"username":username})

def regist(request):
    if request.method == "GET":
        return render(request, "axf/mine/regist.html")
    else:
        if request.is_ajax():
            userAccount = request.POST.get("userAccount")
            try:
                user = User.objects.get(userAccount = userAccount)
                #用户账号已经被占用
                return JsonResponse({"data":1})
            except User.DoesNotExist as e:
                #该用户账号可用
                return JsonResponse({"data": 0})
        else:
            userAccount = request.POST.get("userAccount")
            userPass = request.POST.get("userPass")
            userName = request.POST.get("userName")
            userPhone = request.POST.get("userPhone")
            userAdderss = request.POST.get("userAdderss")
            userImg = ""
            userRank = 1
            userToken = str(random.randrange(1,100000) + time.time())

            #创建用户
            user = User.createuser(userAccount,userPass,userName,userPhone,userAdderss,userImg,userRank,userToken)
            user.save()

            request.session["username"] = userName
            response = redirect("/mine/")
            response.set_cookie("name","username")
            response.set_cookie("token", userToken)
            return response
#退出
def quit(request):
    logout(request)
    response = redirect('/mine/')
    #删除token
    response.delete_cookie("token")
    return response

def loginaxf(request):
    if request.method == "GET":
        return render(request, "axf/mine/login.html")
    else:
        username = request.POST.get("username")
        passwd   = request.POST.get("passwd")
        try:
            user = User.objects.get(userAccount=username)
        except User.DoesNotExist as e:
            return redirect("/loginaxf/")

        if passwd != user.userPasswd:
            return redirect("/loginaxf/")

        #登陆成功
        #重新生成token
        userToken = str(random.randrange(1, 100000) + time.time())
        user.userToken = userToken
        user.save()

        response = redirect("/mine/")
        response.set_cookie("token", userToken)

        #状态保持
        request.session["username"] = user.userName
        response.set_cookie("name", "username")

        return response



#修改购物车
def changeCart(request, flag):
    # 验证是否登录
    token = request.COOKIES.get("token")
    if not token:
        return JsonResponse({"data":-1})

    num = 1
    if flag == "sub":
        num = -1

    # 找到商品
    productid = request.POST.get("productid")
    product = Goods.objects.get(productid=productid)

    #内库存
    if product.storenums == 0 and flag == "add":
        return JsonResponse({"data":-2})

    # 找到当前用户
    currentUser = User.objects.get(userToken=token)

    #找到可用的订单
    try:
        order = Order.objects.filter(user=currentUser).get(isActive=True)
    except Order.DoesNotExist as e:
        if flag == "add":
            orderid = str(random.randrange(1,10000)) + currentUser.userAccount
            order = Order.createOrder(orderid,currentUser)
            order.save()

    #测试
    # cart = Cart.createCart(currentUser, product, num,10,order)
    # cart.save()

    try:
        onecart = Cart.objects.filter(user=currentUser).get(product=product)
        if flag == "chose":
            onecart.ischose = not onecart.ischose
        else:
            onecart.productNum += num
            onecart.productPrice = onecart.productNum * float(product.price)
            product.storenums -= num
            product.save()
        onecart.save()
        if onecart.productNum == 0:
            onecart.delete()
            return JsonResponse({"data": 0})
        return JsonResponse({"data": onecart.productNum,"price":onecart.productPrice,"ischose":onecart.ischose})
    except Cart.DoesNotExist as e:
        if flag == "add":
            onecart = Cart.createCart(currentUser, product, 1, float(product.price), order)
            onecart.save()
            product.storenums -= num
            product.save()
            return JsonResponse({"data": onecart.productNum,"price":onecart.productPrice,"ischose":onecart.ischose})
    return JsonResponse({"data":0})



def downorder(request):
    #找到当前用户
    token = request.COOKIES.get("token")
    currentUser = User.objects.get(userToken=token)
    #得到需要下到订单表中的购物车数据
    carts = Cart.objects.filter(user__userToken=token).filter(ischose=True)

    if len(carts) == 0:
        return redirect("/cart/")


    #将购物车中的对应数据的ischose变为False,isDelete变为True
    for cart in carts:
        cart.ischose = False
        cart.isDelete = True
        cart.save()

    order = Order.objects.filter(user__userToken=token).get(isActive=True)
    #将该订单设置为不活跃订单
    order.isActive = False
    order.progress = 1
    order.save()

    yucarts = Cart.objects.filter(user__userToken=token)
    if len(yucarts) > 0:
        orderid = str(random.randrange(1, 10000)) + currentUser.userAccount
        neworder = Order.createOrder(orderid, currentUser)
        neworder.save()
        for c in yucarts:
            c.order = neworder
            c.save()

    return redirect("/cart/")




