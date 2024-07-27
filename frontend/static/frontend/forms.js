
$(function(){

    $(document).on('formCreated', function(e, formElement){
        dialog = document.querySelector('dialog');
        dialog.showModal();

        $(formElement).on('submit', function(){
            $('.selected').each(function(){
                $(this).removeClass('selected');
            });
        });
    });

    htmx.on('htmx:afterSettle', function(evt) {
        // Check if the added content contains a form with class 'grey-form'
        let addedForm = $(evt.detail.elt).find('.grey-form');
        if (addedForm.length > 0) {
            // Trigger the custom event
            $(document).trigger('formCreated', [addedForm[0]]);
        }
    });

})



