$(document).ready(function(){
    var TABLE_STR = ''
    + '<tr>'
    + '<td><input type="text" class="form-control"></td>'
    + '<td><input type="text" class="form-control"></td>'
    + '<td><button class="btn btn-xs table-remove-btn" type="button"><span class="glyphicon glyphicon-remove"></span></button></td>'
    + '</tr>';
    $('table').delegate('.table-add-btn', 'click', function(){
        $(this).parent().parent().parent().parent().children('tbody').append(TABLE_STR);
    });
    $('table').delegate('.table-remove-btn', 'click', function(){
        $(this).parent().parent().remove();
    });
    $('#submit-driver-add-btn').click(function(){
        set_driver_keys_value();
        var url = document.getElementById('driver-add-form').action;
        $.post(url, $('#driver-add-form').serialize(), function(data){
            data = eval(data);
            if(data[0] === 0){
                window.location.href = '/driver/'+data[1];
            }else{
                alert('Add driver failed!!!/nError Info:'+data[1]);
                return false;
            }
        });
    });
});
function set_driver_keys_value(){
    var params_tr_list = $('#driver-params-table').children('tbody').find('tr');
    var params = {};
    for(var i = 0; i < params_tr_list.length; i++){
        var input_list = $(params_tr_list[i]).find('input');
        var key = $(input_list[0]).val();
        var value = $(input_list[1]).val();
        params[key] = value;
    }
    $('#driver-keys-add').val(JSON.stringify(params));
}
