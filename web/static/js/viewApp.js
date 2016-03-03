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
});
