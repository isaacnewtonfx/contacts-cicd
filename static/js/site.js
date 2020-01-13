var base_url = window.location.protocol + "//" + window.location.host + "/";

$(document).ready(function(){

    $('[data-toggle=popover]').popover({
        content: $('#AccountPopoverContent').html(),
        html: true,
        placement:'bottom'

    }).click(function() {
        $(this).popover('show');
    });

});//end of file