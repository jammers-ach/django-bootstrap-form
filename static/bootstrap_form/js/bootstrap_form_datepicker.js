$(function(){
    $('.datepicker').datetimepicker({
    });
    $('.datetimepicker').datetimepicker({
    });
    $('.datetimepicker input').focus(function(e){
        $(this).parent().datetimepicker('show');
    });
    $('.datetimepicker input').focusout(function(e){
        $(this).parent().data("DateTimePicker").hide();
    });
});
