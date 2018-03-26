$(document).ready(function () {
    //验证
    $("#accunt").bind("blur", function () {
        //验证用户名长度
        if ($(this).val().length < 6 || $(this).val().length > 13) {
            //显示提示信息
            $("#accunterr").show();
            return;
        }
        //验证账号是否可用，后台验证
        $.post("/regist/", {"userAccount":$(this).val()}, function (data, status) {
            if (data.data){
                //有问题
                $("#checkerr").show();
            }
        })
    });
    $("#accunt").bind("focus", function () {
        $(this).val("");
        $("#accunterr").hide();
        $("#checkerr").hide();
    });
});