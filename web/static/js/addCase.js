$(document).ready(function(){
    var driver_map = $('#driver_map').val();
    driver_map = JSON.parse(driver_map);
    $('#driver-select').change(function(){
        var driver_name = $(this).val();
        params = driver_map[driver_name]['param'];
        params_str = JSON.stringify(params);
        $('#case_param_add').val(params_str);
    });
    $('#submit-case-add-btn').click(function(){
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
function set_case_param(){
    var params_tr_list = $('#case-params-table').children('tbody').find('tr');
    var params = {};
    for(var i = 0; i < params_tr_list.length; i++){
        var input_list = $(params_tr_list[i]).find('input');
        var key = $(input_list[0]).val();
        var value = $(input_list[1]).val();
        params[key] = value;
    }
    $('#driver-keys-add').val(JSON.stringify(params));
}
