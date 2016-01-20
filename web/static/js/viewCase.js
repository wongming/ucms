$(document).ready(function(){
    var is_executed = $('#is_executed').val();
    var case_name = $('#case_name').val();
    if (is_executed=="True"){
        pageListShow({"postUrl":"/case/"+case_name+"/result"});
    }
    $('#run_case').click(function(){
        var url = document.getElementById('case_add_form').action;
        $.post(url, $('#case_add_form').serialize(), function(data){
            data = eval(data);
            if(data[0] === 0){
                window.location.href = '/case/'+data[1];
            }else{
                alert('Add case failed!!!/nError Info:'+data[1]);
                return false;
            }
        });
    });
});
