$(document).ready(function(){
    //黄色小方块
    var urlstr = location.href;
    arr = urlstr.split("/");
    $span = $(document.getElementById(arr[4]));
    $span.addClass("yellowSlide");



    $("#alltypebtn").bind("click", function () {
        $("#typeDiv").toggle();
        $("#sortDiv").hide();
    });
    $("#sortbtn").bind("click", function () {
        $("#typeDiv").hide();
        $("#sortDiv").toggle();
    });


    function  selfhide() {
        $(this).hide()
    }
    $("#typeDiv").bind("click", selfhide);
    $("#sortDiv").bind("click", selfhide);



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
            }
        });
    });

});