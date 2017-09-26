/**
 * Created by Anonymous on 2017/9/26.
 */

$(".uptitleedit").click(function () {
     $("#UPmyModal").modal();
    var upid= $(this).attr("id");
    $("#upid").val(upid);
});

$(".delid").click(function () {
    $("#delcfmModel").modal();
    var delid= $(this).attr("id");
    $("#delid").val(delid);
});