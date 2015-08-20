$( document ).ready(function(){
    $( ".select2" ).select2();

    $('#datetimepicker2').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD HH:mm:ss'
    });
})