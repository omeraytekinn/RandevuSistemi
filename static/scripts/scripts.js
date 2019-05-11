$(document).ready(function () {
  $('#btnDuzenle').click(function(){
    $('#btnKaydet').show();
    $('#btnIptal').show();
    $('#btnDuzenle').hide();
    $('form .form-row input, form textarea').removeAttr('readonly');
    $('form .form-row input, form textarea').removeClass('form-control-plaintext');
    $('form .form-row input, form textarea').addClass('form-control');
  });
  $('#btnIptal').click(function(){
    $('#btnKaydet').hide();
    $('#btnIptal').hide();
    $('#btnDuzenle').show();
    $('form .form-row input, form textarea').attr('readonly',"");
    $('form .form-row input, form textarea').addClass('form-control-plaintext');
    $('form .form-row input, form textarea').removeClass('form-control');
  });
});
