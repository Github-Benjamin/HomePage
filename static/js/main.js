/**
 * Created by Anonymous on 2017/9/26.
 */

$('.userinfo').click(function () {
    $("#myModal").modal();
});

$('.xiugai').click(function () {
    $("#UPPassWord").modal();
});

// ifame框架打开页面
var openpage = function (href) {
    $(".addpage").empty();
    var html = '<iframe id="iframe-page-content" src="'+href+'" width="100%"  frameborder="no" border="0" marginwidth="0" marginheight=" 0" scrolling="no" allowtransparency="yes"></iframe>'
    $(".addpage").append(html);
    var ifm= document.getElementById("iframe-page-content");
    ifm.height=document.documentElement.clientHeight+220;
}

//加载ifame框架
$(".addmeu").click(function(){
    var href= $(this).attr("data-href");
    openpage(href);
});

// 图片预览,鼠标移上时触发弹出提示框，开启html 为true的话，data-content里就能放html代码了
$("[data-toggle='popover']").popover({
    trigger : 'hover',
    html:true,
});

// 修改Banner操作
$(".upbanneredit").click(function () {
     $("#upBanner").modal();
     $(".alert-warning").remove()
    var upid= $(this).attr("id");
    var img= $(this).attr("data-img");
    var title= $(this).attr("data-title");
    var a= $(this).attr("data-a");
    var p= $(this).attr("data-p");
    xupstatus = $(this).attr("data-status");
    var status = xupstatus;
    $("#upid").val(upid);
    $("#uptitle").val(title);
    $("#uplink").val(a);
    $("#upcontent").val(p);
    $("#upstatus").val(status);
    $(".upimg").empty();
    $(".upimg").append('<img src="'+img+'" alt="" style="width: 300px;margin-top: 10px">');
});



var statuscount = $("#statuscount").attr("value");

// 新增,不允许提交大于4个启用状态的Banner图
$('.checkstatus').click(function () {
    var status = document.getElementById("status").value;
    if ((parseInt(statuscount)+parseInt(status))>4){
         $(".alert-warning").remove()
         $("#status").after('<div class="alert alert-warning" style="width:250px;margin-top: 15px"><a href="#" class="close" data-dismiss="alert">&times;</a><strong>警告！</strong>Banner最多设置4个启用</div>');
         return false;
    }
});

// 修改,不允许提交大于4个启用状态的Banner图
$('.checkupstatus').click(function () {
    if (xupstatus==1){
    }else {
        var upstatus = document.getElementById("upstatus").value;
        if ((parseInt(statuscount)+parseInt(upstatus))>4){
                 $(".alert-warning").remove()
                 $("#upstatus").after('<div class="alert alert-warning" style="width:250px;margin-top: 15px"><a href="#" class="close" data-dismiss="alert">&times;</a><strong>警告！</strong>Banner最多设置4个启用</div>');
                 return false;
        }
    }
});


// 修改电影弹窗操作
$(".uptitleedit").click(function () {
     $("#UPmyModal").modal();
    var upid= $(this).attr("id");
    var img= $(this).attr("data-img");
    var title= $(this).attr("data-title");
    var content= $(this).attr("data-content");
    var link= $(this).attr("data-link");
    var a= $(this).attr("data-a");
    $("#upid").val(upid);
    $("#uptitle").val(title);
    $("#upcontent").val(content);
    $("#uplink").val(a);
    $("#uplinks").val(link);
    $(".upimg").empty();
    $(".upimg").append('<img src="'+img+'" alt="" style="width: 300px;margin-top: 10px">');
});


// 修改资讯操作
$(".UPbullhorn").click(function () {
     $("#UPbullhorn").modal();
    var upid= $(this).attr("id");
    var img= $(this).attr("data-img");
    var title= $(this).attr("data-title");
    var content= $(this).attr("data-content");
    var publisher= $(this).attr("data-publisher");
    var times= $(this).attr("data-times");
    var a_link= $(this).attr("data-a_link");
    var hot_id= $(this).attr("data-hot_id");
    $("#upid").val(upid);
    $("#uptitle").val(title);
    $("#upcontent").val(content);
    $("#uplink").val(a_link);
    $("#uppublisher").val(publisher);
    $("#uptimes").val(times);
    $("#uphot_id").val(hot_id);
    $(".upimg").empty();
    $(".upimg").append('<img src="'+img+'" alt="" style="width: 300px;margin-top: 10px">');
});

// 删除Banner、电影操作
$(".delid").click(function () {
    $("#delcfmModel").modal();
    var delid= $(this).attr("id");
    $("#delid").val(delid);
});



// 修改用户信息操作
$(".upusermanage").click(function () {
    var upid= $(this).attr("id");
    var username= $(this).attr("data-username");
    var email= $(this).attr("data-email");
    var phone= $(this).attr("data-phone");
    var role= $(this).attr("data-role");
    $("#upid").val(upid);
    $("#upusername").val(username);
    $("#upemail").val(email);
    $("#upphone").val(phone);
    $("#uprole").val(role);
    $("#UPmyModal").modal();
});


// 启用操作
$(".enable").click(function () {
    $("#delcfmModel").modal();
    var delid= $(this).attr("id");
    $('#uesrstaus').empty().append('启用')
    $("#delid").val(delid);
    $("#deluesrstaus").attr("value","1");
});


// 停用操作
$(".disable").click(function () {
    $("#delcfmModel").modal();
    var delid= $(this).attr("id");
    $('#uesrstaus').empty().append('停用')
    $("#delid").val(delid);
    $("#deluesrstaus").attr("value","0");
});

// 修改新闻操作
$(".upnews").click(function () {
    var upid= $(this).attr("id");
    var uptitle= $(this).attr("data-title");
    var upauthor= $(this).attr("data-author");
    var uptime= $(this).attr("data-uptime");

    $.ajax({
            type: "GET",
            url: "admins/news",
            dataType:'json',
            data:{"queryid":upid},
            success: function(data){
                    if (data["success"]) {
                        callbackeditor.html(data["success"]);
                    }
            },
            error: function (data) {
                $(".alert-warning").remove();
                $(".error").append('<div class="alert alert-warning" id="error" style="display: block;width: 280px"> <a href="#" class="close" data-dismiss="alert">&times;</a> <strong>警告！</strong>您的网络连接有问题。 </div>');
            }
        });


    $("#upid").val(upid);
    $("#uptitle").val(uptitle);
    $("#upauthor").val(upauthor);
    $("#upselecttime").val(uptime);
    $("#UPmyModal").modal();
});



