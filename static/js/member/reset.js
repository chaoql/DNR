;
var member_reset_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".do-reset").click(function () { // 前面带"$"的就是jQuery语句
            const btn_target = $(this);
            if(btn_target.hasClass("disabled")){ // 避免重复点击注册
                common_ops.alert("正在处理！请勿重复点击~~");
                return ;
            }
            const old_pwd = $(".reset-wrap input[name=old_password]").val();
            const new_pwd = $(".reset-wrap input[name=new_password]").val();
            const new_pwd2 = $(".reset-wrap input[name=new_password2]").val();
            if (old_pwd === undefined || old_pwd.length < 6) {
                common_ops.alert("请输入正确的旧登陆密码~~");
                return;
            }
            if (new_pwd === undefined || new_pwd.length < 6) {
                common_ops.alert("请输入正确的新登陆密码，并且不能小于6个字符~~");
                return;
            }
            if (new_pwd2 === undefined || new_pwd2 !== new_pwd) {
                common_ops.alert("请输入正确的确认新登陆密码~~");
                return;
            }
            btn_target.addClass("disabled");
            // ajax是一种数据请求的方式，不需要刷新整个页面。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新c
            $.ajax({
                // url: "/member/reg", // 前端路由地址，全称为：http://192.168.0.108:5000/member/reg
                url: common_ops.buildUrl("/member/reset"),
                type: "POST",
                data:{
                    old_pwd:old_pwd,
                    new_pwd:new_pwd,
                    new_pwd2:new_pwd2,
                },
                dataType:'json', // 返回值格式
                success:function (res){ // 请求成功后执行的代码
                    btn_target.removeClass("disabled");
                    let callback = null;
                    if(res.code === 200){
                        callback=function (){
                            window.location.href=common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};

$(document).ready(function () {
    member_reset_ops.init();
});