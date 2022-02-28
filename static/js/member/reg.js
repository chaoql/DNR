;
var member_reg_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".do-reg").click(function () { // 前面带"$"的就是jQuery语句
            const btn_target = $(this);
            if(btn_target.hasClass("disabled")){ // 避免重复点击注册
                common_ops.alert("正在处理！请勿重复点击~~");
                return ;
            }
            const nick_name = $(".reg-wrap input[name=nick_name]").val();
            const login_name = $(".reg-wrap input[name=login_name]").val();
            const login_pwd = $(".reg-wrap input[name=login_pwd]").val();
            const login_pwd2 = $(".reg-wrap input[name=login_pwd2]").val();
            if (nick_name == undefined || nick_name.length < 1) {
                common_ops.alert("请输入正确的昵称~~");
                return;
            }
            if (login_name == undefined || login_name.length < 1) {
                common_ops.alert("请输入正确的登陆用户名~~");
                return;
            }
            if (login_pwd == undefined || login_pwd.length < 6) {
                common_ops.alert("请输入正确的登陆密码，并且不能小于6个字符~~");
                return;
            }
            if (login_pwd2 == undefined || login_pwd2 != login_pwd) {
                common_ops.alert("请输入正确的确认登陆密码~~");
                return;
            }
            btn_target.addClass("disabled");
            // ajax是一种数据请求的方式，不需要刷新整个页面。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新c
            $.ajax({
                // url: "/member/reg", // 前端路由地址，全称为：http://192.168.0.108:5000/member/reg
                url: common_ops.buildUrl("/member/reg"),
                type: "POST",
                data:{
                    nick_name:nick_name,
                    login_name:login_name,
                    login_pwd:login_pwd,
                    login_pwd2:login_pwd2,
                },
                dataType:'json', // 返回值格式
                success:function (res){ // 请求成功后执行的代码
                    btn_target.removeClass("disabled");
                    var callback=null;
                    if(res.code == 200){
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
    member_reg_ops.init();
});