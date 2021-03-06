$(document).ready(function(){
    var is_executed = $('#is_executed').val();
    var plan_name = $('#plan_name').val();
    var plan_id = $('#plan_id').val();
    if (is_executed=="True"){
        pageListShow({"postUrl":"/plan/"+plan_name+"/result"});
    }
    $('#run_plan').click(function(){
        if(confirm("Run test plan?")){
            $.post("/plan/"+plan_id+"/run", {}, function(data){
                data = eval(data);
                if(data[0] === 0){
                    location.href = '/plan/'+plan_id;
                }else{
                    alert('Run plan failed!!!/nError Info:'+data[1]);
                    return false;
                }
            });
        }
        return false;
    });
    $('#del_plan').click(function(){
        var url = '/plan/'+plan_id+'/del';
        $.post(url, {}, function(data){
            data=eval(data);
            if(data[0]==0){
                alert('删除plan成功！');
                location.href = '/plan';
            }else{
                alert('删除plan失败！');
            }
        })
    });
});
