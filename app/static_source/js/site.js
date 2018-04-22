$(function() {
    $('.datepicker').datepicker({});
});

function toggleVisibility(elem) {
  $(elem).find('.password').toggle();
  $(elem).find('.btn').toggle();
}
