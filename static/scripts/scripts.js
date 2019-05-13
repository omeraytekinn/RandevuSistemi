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

  $('#notifyModal').modal({show:true, backdrop: false});
  setTimeout(function() {
    $('#notifyModal').modal('hide');
  }, 2500);
  $('#notifyModal').click(function() {
      $('#notifyModal').modal('hide');
  });


    $('#dtBasicExample').DataTable( {
          "infoEmpty": "No entries to show",
          language: {
            "decimal":        "",
            "emptyTable":     "Veri bulunamadı!",
            "info":           "_TOTAL_ öğretmenden _START_ ile _END_ arasındakiler gösteriliyor",
            "infoEmpty":      "",
            "infoFiltered":   "",
            "infoPostFix":    "",
            "thousands":      ",",
            "lengthMenu":     "Öğretim Üyeleri  ",
            "loadingRecords": "Yükleniyor...",
            "processing":     "İşleniyor...",
            "search":         "Ara:",
            "zeroRecords":    "İstenen kayıt bulunamadı",
            "paginate": {
                "first":      "<<",
                "last":       ">>",
                "next":       ">",
                "previous":   "<"
            },
            "aria": {
                "sortAscending":  ":",
                "sortDescending": ":"
            }
          },
      columns:[
        	{
            	"sortable": false
            },
            {
            	"sortable": true
            },
            {
            	"sortable": false
            },
            {
            	"sortable": false
            },
            {
            	"sortable": false
            }
        ]
    });

    var profilid;
    $(".profil-btn").click(function(){
      profilid = $(this).attr("name");
      $.ajax({
        url: 'get/profile/'+profilid,
        success: function(data) {
            $('#profile-modal .modal-icerik').html(data.name);
        }
      });
    });

});
