$(document).ready(function(){
    $('#add-plan-submit-btn').click(function(){
        var url = document.getElementById('add_plan_form').action;
        $.post(url, $('#add_plan_form').serialize(), function(data){
            data = eval(data);
            if(data[0] === 0){
                window.location.href = '/plan/'+data[1];
            }else{
                alert('Add case failed!!!/nError Info:'+data[1]);
                return false;
            }
        });
    });
});
