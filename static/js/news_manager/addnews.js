;
var member_add_ops = {
    init: function () {
        this.eventBind();
    },
    eventBind: function () {
        $(".do-add").click(function () { // 前面带"$"的就是jQuery语句
            const btn_target = $(this);
            if (btn_target.hasClass("disabled")) { // 避免重复点击注册
                common_ops.alert("正在处理！请勿重复点击~~");
                return;
            }
            const title = $(".add-wrap input[name=title]").val();
            const genre = $(".add-wrap input[name=genre]").val();
            const authors = $(".add-wrap input[name=authors]").val();
            const date = $(".add-wrap input[name=date]").val();
            const view = $(".add-wrap input[name=view]").val();
            const link = $(".add-wrap input[name=link]").val();
            const r = /^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$/;
            const http_r = /^(http|https):\/\/([\w-]+\.)+[\w-]+(\/[\w-.\/?%&=]*)?$/;
            const genre_list = ["antip", "ent", "milite", "world", "tech", "finance"];
            let genre_flag = 0;
            if (title === undefined || title.length < 1) {
                common_ops.alert("请输入正确的新闻题目~~~");
                return;
            }
            for (let i = 0; i < genre_list.length; i++) {
                if (genre === genre_list[i]){
                    genre_flag = 1;
                    break;
                }
            }
            if ((genre.length >= 1 && genre_flag === 0) || (genre === undefined || genre.length < 1)) {
                common_ops.alert("请选择正确的新闻类别~~~");
                return;
            }
            if (authors === undefined || authors.length < 1) {
                common_ops.alert("请输入正确的作者~~~");
                return;
            }
            if(!http_r.test(link)){
                common_ops.alert("请输入正确的数据来源链接~~~");
                return;
            }
            if(!r.test(date)){
                common_ops.alert("请输入正确的时间格式，如：2022-03-18 17:12:00~~~");
                return;
            }
            if (view === undefined || view.length < 1) {
                common_ops.alert("请输入正确的新闻阅读数~~~");
                return;
            }
            btn_target.addClass("disabled");
            // ajax是一种数据请求的方式，不需要刷新整个页面。这意味着可以在不重新加载整个网页的情况下，对网页的某部分进行更新c
            $.ajax({
                // url: "/member/reg", // 前端路由地址，全称为：http://192.168.0.108:5000/member/reg
                url: common_ops.buildUrl("/newsManager/add"),
                type: "POST",
                data: {
                    title:title,
                    genre:genre,
                    authors: authors,
                    date: date,
                    view: view,
                    link: link,
                },
                dataType: 'json', // 返回值格式
                success: function (res) { // 请求成功后执行的代码
                    btn_target.removeClass("disabled");
                    var callback = null;
                    if (res.code == 200) {
                        callback = function () {
                            window.location.href = common_ops.buildUrl("/newsManager/newstext");
                        }
                    }
                    common_ops.alert(res.msg, callback);
                }
            })
        });
    }
};

$(document).ready(function () {
    member_add_ops.init();
});