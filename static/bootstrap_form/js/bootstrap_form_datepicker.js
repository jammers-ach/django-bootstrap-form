$(function(){
    $('.datepicker').datetimepicker({
        pickTime:false,
    });
    $('.datetimepicker').datetimepicker({
        sideBySide:true,
    });
    $('.datetimepicker input').focus(function(e){
        $(this).parent().data("DateTimePicker").show();
    });
    $('.datetimepicker input').focusout(function(e){
        $(this).parent().data("DateTimePicker").hide();
    });
});
