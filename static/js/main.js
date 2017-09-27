/**
 * Created by Anonymous on 2017/9/26.
 */

// ifame框架打开页面
var openpage = function (href) {
    $(".addpage").empty();
    var html = '<iframe id="iframe-page-content" src="'+href+'" width="100%"  frameborder="no" border="0" marginwidth="0" marginheight=" 0" scrolling="no" allowtransparency="yes"></iframe>'
    $(".addpage").append(html);
    var ifm= document.getElementById("iframe-page-content");
    ifm.height=document.documentElement.clientHeight+100;
}


//加载ifame框架
$(".addmeu").click(function(){
    var href= $(this).attr("data-href");
    openpage(href);
});



// 修改电影弹窗操作
$(".uptitleedit").click(function () {
     $("#UPmyModal").modal();
    var upid= $(this).attr("id");
    var img= $(this).attr("data-img");
    var title= $(this).attr("data-title");
    var a= $(this).attr("data-a");
    $("#upid").val(upid);
    $("#uptitle").val(title);
    $("#uplink").val(a);
    $(".upimg").empty();
    $(".upimg").append('<img src="'+img+'" alt="" style="width: 300px;margin-top: 10px">');
});

// 删除电影操作
$(".delid").click(function () {
    $("#delcfmModel").modal();
    var delid= $(this).attr("id");
    $("#delid").val(delid);
});

// 图片预览,鼠标移上时触发弹出提示框，开启html 为true的话，data-content里就能放html代码了
$("[data-toggle='popover']").popover({
    trigger : 'hover',
    html:true,
});