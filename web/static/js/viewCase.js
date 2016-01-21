$(document).ready(function(){
    var is_executed = $('#is_executed').val();
    var case_name = $('#case_name').val();
    var case_id = $('#case_id').val();
    if (is_executed=="True"){
        pageListShow({"postUrl":"/case/"+case_name+"/result"});
    }
    $('#run_case').click(function(){
        if(confirm("Run test case?")){
            $.post("/case/"+case_id+"/run", {}, function(data){
                data = eval(data);
                if(data[0] === 0){
                    location.href = '/case/'+case_id;
                }else{
                    alert('Run case failed!!!/nError Info:'+data[1]);
                    return false;
                }
            });
        }
        return false;
    });
});
