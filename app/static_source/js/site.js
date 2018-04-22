$(function() {
    $('.datepicker').datepicker({});
});

function toggleVisibility(elem) {

    if ( $(elem).find('span').css('visibility') == 'hidden' ) {
        $(elem).find('span').css('visibility', 'visible');
    }
    else {
        $(elem).find('span').css('visibility', 'hidden');
    }
}
