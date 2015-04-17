/**
 * Easy to use yes/no/cancel boxes using bootstrap
 */

/**
 * Pops up a little yes_no box
 * calls function_if_yes, if yes is pressed
 * function_if_yes can be a function pointer
 * or an [object,attribute_name]
 */
function bs_show_yes_no(message,title,function_if_yes){
    var m =$('#warning_modal');
    m.modal();
    m.find('.modal-dialog').css('z-index','10000');
    m.find('.modal-title').html(title);
    m.find('.modal-body').html(message);


    if(typeof(function_if_yes) == "function"){
        $("#modal_warning_yes").unbind('click').bind('click',function_if_yes);
    }else{
        $("#modal_warning_yes").unbind('click').bind('click',function(){
            function_if_yes[0][function_if_yes[1]]();
        });

    }
}


$(function(){
    //First of all, stick the boxes to the main page

var warning_modal = $(' \
<div class="modal " id="warning_modal"> \
  <div class="modal-dialog"> \
    <div class="modal-content"> \
      <div class="modal-header"> \
        <button type="button" class="close" data-dismiss="modal" aria-label="Close"><span aria-hidden="true">&times;</span></button> \
        <h4 class="modal-title">Modal title</h4> \
      </div> \
      <div class="modal-body"> \
      </div> \
      <div class="modal-footer"> \
        <button id="modal_warning_yes" type="button" class="btn btn-primary" data-dismiss="modal">Yes</button> \
        <button id="modal_warning_no" type="button" class="btn btn-default" data-dismiss="modal">No</button> \
      </div> \
    </div><!-- /.modal-content --> \
  </div><!-- /.modal-dialog --> \
</div><!-- /.modal --> \
')
    $('body').prepend(warning_modal);
});
