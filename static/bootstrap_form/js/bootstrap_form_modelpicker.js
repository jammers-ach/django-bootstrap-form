var modal = '\
<div class="modal fade" id="add_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
  <div class="modal-dialog">\
    <div class="modal-content">\
      <div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>\
        <h4 class="modal-title" id="myModalLabel">Add</h4>\
      </div>\
      <div class="modal-body">\
        ...\
      </div>\
      <div class="modal-footer">\
        <button type="button" class="btn btn-default" data-dismiss="modal">Close</button>\
        <button type="button" class="btn btn-primary" id="add_button">Add</button>\
      </div>\
    </div>\
  </div>\
</div>\
'

var modal2 = '\
<div class="modal fade" id="search_modal" tabindex="-1" role="dialog" aria-labelledby="myModalLabel" aria-hidden="true">\
  <div class="modal-dialog">\
    <div class="modal-content">\
      <div class="modal-header">\
        <button type="button" class="close" data-dismiss="modal"><span aria-hidden="true">&times;</span><span class="sr-only">Close</span></button>\
        <h4 class="modal-title" id="myModalLabel">Search</h4>\
      </div>\
      <div class="modal-body">\
        ...\
      </div>\
    </div>\
  </div>\
</div>\
'


$(function(){

    $('body').prepend(modal);
    $('body').prepend(modal2);

    $('.search_obj_button').click(function(e){
        $('#search_modal').modal();
        var url = $(this).attr('data-url');
        var parent_input = $(this).closest('.model-picker').find('select');
        $.ajax({
            url:url,
            data:'ajax=true',
        }).done(function(data){
            console.log(data);
            $('#search_modal .modal-body').html(data);
            $('#search_modal .modal-body a.search_go_link').click(function(e){
                parent_input.val($(this).attr('data-id'));

                $('#search_modal').modal('hide');
            });
        });
    });

    $('.add_obj_button').click(function(e){
        $('#add_modal').modal();
        $('#add_button').unbind('click');
        var url = $(this).attr('data-url');
        var parent_input = $(this).closest('.model-picker').find('select');
        $.ajax({
            url:url,
            data:'ajax=true',
        }).done(function(data){
            $('#add_modal .modal-body').html(data);
            $('#add_button').click(function(){
                var form = $('#add_modal .modal-body form');
                $.ajax({
                    type:'POST',
                    url:url,
                    data:form.serialize(),
                }).done(function(data){
                    if(data.lastIndexOf('OK',0) == 0){
                        //The id and object repr are in the 2nd line of response
                        var info = data.split('\n')[1].split(',');
                        parent_input.append('<option value="'+info[0]+'">'+info[1]+'</option>');
                        parent_input.val(info[0]);
                        $('#add_modal').modal('hide');
                    }else{
                        $('#add_modal .modal-body').html(data);
                    }
                });
            });
        });
    });
})
