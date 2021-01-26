$('#message').hide();
$('#password, #confirm_password').on('keyup', function () {
  if ($('#password').val() == $('#confirm_password').val()) {
    $('#confirm_password').css('border-color', 'lime');
    $('#password').css('border-color', 'lime');
    $('#message').hide();
  }
  else{
    $('#confirm_password').css('border-color', 'red');
    $('#password').css('border-color', 'red');
    $('#message').show();}

});
