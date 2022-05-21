;
var member_forgot_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".do-forgot").click(function () { // 前面带"$"的就是jQuery语句
            const btn_target = $(this);
            if (btn_target.hasClass("disabled")) { // 避免重复点击注册
                common_ops.alert("正在处理！请勿重复点击~~");
                return;
            }
            const name = $(".forgot-wrap input[name=name]").val();
            if (name === undefined || name.length < 1) {
                common_ops.alert("请选择正确的用户名~~");
                return;
            }
            btn_target.addClass("disabled");
            // ajax是一种数据请求的方式，不需要刷新整个页面。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新c
            $.ajax({
                // url: "/member/reg", // 前端路由地址，全称为：http://192.168.0.108:5000/member/reg
                url: common_ops.buildUrl("/member/forgot"),
                type: "POST",
                data: {
                    name: name,
                },
                dataType: 'json', // 返回值格式
                success: function (res) { // 请求成功后执行的代码
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code === 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};

$(document).ready(function () {
    member_forgot_ops.init();
});