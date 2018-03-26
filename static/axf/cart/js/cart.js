$(document).ready(function () {
        //点击加号，添加购物车
    $allAddBtn = $(".addShopping")
    $allSubBtn = $(".subShopping")

    $allAddBtn.bind("click", function () {
        //获取到点击商品的productid
        var productid = $(this).attr("pd")
        //将商品id发送给后台
        $.post("/changeCart/add/", {"productid":productid}, function (data, status) {
            if (data.data == -1) {
                location.href = "http://127.0.0.1:8000/loginaxf/"
            } else if (data.data == -2) {

            } else {
                //找到span
               $(document.getElementById("num"+productid)).html(data.data+"")
                //修改钱
                $(document.getElementById("price"+productid)).html(data.price+"")
            }
        });
    });




    $allSubBtn.bind("click", function () {
        //获取到点击商品的productid
        var productid = $(this).attr("pd")
        //将商品id发送给后台
        $.post("/changeCart/sub/", {"productid":productid}, function (data, status) {
            if (data.data == -1) {
                location.href = "http://127.0.0.1:8000/loginaxf/"
            } else if (data.data >= 0) {
                //找到span
                $(document.getElementById("num"+productid)).html(data.data+"")
                $(document.getElementById("price"+productid)).html(data.price+"")
                if (data.data == 0) {
                    // $("#productlistul").remove($(document.getElementById("li"+productid)))
                    document.getElementById("productlistul").removeChild(document.getElementById("li"+productid))
                }
            }
        });
    });



    $(".ischose").bind("click", function () {
        var productid = $(this).attr("pd")
        $.post("/changeCart/chose/", {"productid":productid}, function (data, status) {
            var str = ""
            if (data.ischose) {
                str = "√"
            }
            $(document.getElementById("chose"+productid)).html(str)
        });
    });
});