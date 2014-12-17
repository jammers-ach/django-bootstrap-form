$(function(){
    $('.otherchoice').change(function(e){
        if($(this).val() == '_-_'){
            var them = $(this).parent().find('.other_option');

            console.log(them);
            them.show().focus();
            var name = them.attr('name');
            them.attr('name',name.substring(2))
            $(this).remove();
        }
    });

});
