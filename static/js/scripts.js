function get_price(url) {
    nomenclature_id = $('#nomenclature_id').val()
    attribute_id = $('#attribute_id').val()
    $.ajax({
        url: url + '?nomenclature=' + nomenclature_id + '&attribute=' + attribute_id,
        dataType: "json",
        success: function(data) {
            if (data.result) {
                $('#outgoing_price').val(data.price)
            }
        }
    })
}

$( document ).ready(function(){
    $( ".select2" ).select2();

    $('#datetimepicker2').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD HH:mm:ss'
    });

    $('.datetimepicker1').datetimepicker({
        locale: 'ru',
        format: 'YYYY-MM-DD'
    });
})