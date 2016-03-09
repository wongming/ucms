$(document).ready(function(){
    var app_id = $('#app_id').val();
    $('#view_release').click(function(){
        if(confirm("Release the application?")){
            $.post("/app/"+app_id+"/release", {}, function(data){
                data = eval(data);
                if(data[0] === 0){
                    location.href = '/app/'+app_id;
                }else{
                    alert('Release the application failed!!!/nError Info:'+data[1]);
                    return false;
                }
            });
        }
        return false;
    });
    $('#del_app').click(function(){
        var url = '/app/'+app_id+'/del';
        $.post(url, {}, function(data){
            data=eval(data);
            if(data[0]==0){
                alert('删除app成功！');
                location.href = '/app';
            }else{
                alert('删除app失败！');
            }
        })
    });
});
