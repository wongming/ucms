$(document).ready(function(){
    var driver_id = $('#driver_id').val();
    $('#del_driver').click(function(){
        var url = '/driver/'+driver_id+'/del';
        $.post(url, {}, function(data){
            data=eval(data);
            if(data[0]==0){
                alert('删除driver成功！');
                location.href = '/driver';
            }else{
                alert('删除driver失败！');
            }
        })
    });
});
