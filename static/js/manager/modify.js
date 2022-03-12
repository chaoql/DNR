;
var member_modify_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".do-modify").click(function () { // 前面带"$"的就是jQuery语句
            const btn_target = $(this);
            if (btn_target.hasClass("disabled")) { // 避免重复点击注册
                common_ops.alert("正在处理！请勿重复点击~~");
                return;
            }
            const nick_name = $(".modify-wrap input[name=nickname]").val();
            const login_name = $(".modify-wrap input[name=login_name]").val();
            const gender = $(".modify-wrap input[name=gender]").val();
            const age = $(".modify-wrap input[name=age]").val();
            const use = $(".modify-wrap input[name=use-power]").val();
            const occupation = $(".modify-wrap input[name=occupation]").val();
            const occ_list = ["Student", "Teacher", "Engineer", "Researcher", "Doctor", "Policeman", "Others"];
            let occ_flag = 0;
            if (nick_name === undefined || nick_name.length < 1) {
                common_ops.alert("请输入正确的昵称~~~");
                return;
            }
            if (use.length >=1 && use !=="using" && use !== "not using"){
                common_ops.alert("请选择正确的用户状态~~~");
                return;
            }
            if (gender.length >= 1 && gender !== "Male" && gender !== "Female") {
                common_ops.alert("请选择正确的性别~~~");
                return;
            }
            if (age === undefined || age.length < 1 || (age > 100 || age < 0)) {
                common_ops.alert("请输入正确的年龄~~~");
                return;
            }
            for (let i = 0; i < occ_list.length; i++) {
                if (occupation === occ_list[i])
                    occ_flag = 1;
            }
            if (occupation.length >= 1 && occ_flag === 0) {
                common_ops.alert("请选择正确的职业~~~");
                return;
            }
            btn_target.addClass("disabled");
            // ajax是一种数据请求的方式，不需要刷新整个页面。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新c
            $.ajax({
                // url: "/member/reg", // 前端路由地址，全称为：http://192.168.0.108:5000/member/reg
                url: common_ops.buildUrl("/manager/co_modify"),
                type: "POST",
                data: {
                    nick_name:nick_name,
                    login_name:login_name,
                    gender: gender,
                    age: age,
                    use: use,
                    occupation: occupation
                },
                dataType: 'json', // 返回值格式
                success: function (res) { // 请求成功后执行的代码
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/manager/");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};

$(document).ready(function () {
    member_modify_ops.init();
});