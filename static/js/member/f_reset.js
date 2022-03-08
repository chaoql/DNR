;
var member_freset_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".do-freset").click(function () { // 前面带"$"的就是jQuery语句
            const btn_target = $(this);
            if(btn_target.hasClass("disabled")){ // 避免重复点击注册
                common_ops.alert("正在处理！请勿重复点击~~");
                return ;
            }
            const target = "?token="
            const strHref = document.location.toString();
            const intPos = strHref.indexOf(target);
            const token = strHref.substr(intPos + 7);
            const new_pwd = $(".freset-wrap input[name=new_password]").val();
            const new_pwd2 = $(".freset-wrap input[name=new_password2]").val();
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
                url: common_ops.buildUrl("/member/f_reset"),
                type: "POST",
                data:{
                    new_pwd:new_pwd,
                    new_pwd2:new_pwd2,
                    token: token,
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
    member_freset_ops.init();
});