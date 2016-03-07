$(document).ready(function(){
    var driver_map = $('#driver_map').val();
    driver_map = JSON.parse(driver_map);
    //初始化时的param table
    init_param_table('case_param_table', driver_map[$('#driver-select').val()]['param'])
    //切换driver时改变param table
    $('#driver-select').change(function(){
        var driver_name = $(this).val();
        params = driver_map[driver_name]['param'];
        init_param_table('case_param_table', params);
    });
    $('#submit-case-add-btn').click(function(){
        var url = document.getElementById('case_add_form').action;
        var param = {};
        tr_list = $('#case_param_table').children('table').children('tbody').children('tr');
        for(var i = 0; i < tr_list.length; i++){
            var key = tr_list[i].cells[0].innerText;
            var value = tr_list[i].cells[1].childNodes[0].value;
            param[key] = value;
        }
        $('#param').val(JSON.stringify(param));
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
function init_param_table(id, params){
    var content = '';
    if(JSON.stringify(params) == '{}') {
        document.getElementById(id).className = 'col-sm-3';
        content +='<label class="form-control">No Params</label>';
    }else{
        document.getElementById(id).className = 'col-sm-6';
        var thead = '<thead class="breadcrumb">' +
                '<tr>' +
                    '<th width="150px">Key Name</th>' +
                    '<th>Default Value</th>' +
                '</tr>' +
            '</thead>';
        params = eval(params);
        var tbody = '<tbody>';
        for(var key in params){
            var tbody_temp = '<tr><td>'+ key + '</td><td><input type="text" class="form-control" value='+params[key]+'>' + '</td></tr>';
            tbody += tbody_temp;
        }
        tbody += '</tbody>';
        content += '<table class="table table-bordered" id="case-params-table">';
        content += thead;
        content += tbody;
        content += '</table>';
    }
    document.getElementById(id).innerHTML = content;
}
