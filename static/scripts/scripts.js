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


    $('#teacherTable').DataTable( {
          "order": [[ 3, "asc" ]],
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
            	"sortable": true
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

    var profilID;
    $(".profile-btn").click(function(){
      profilID = $(this).attr("name");
      $.ajax({
        url: 'get/profile/'+profilID,
        success: function(data) {
          $('#profile-modal .modal-icerik').eq(0).html(data.name);
          $('#profile-modal .modal-icerik').eq(1).html(data.surname);
          $('#profile-modal .modal-icerik').eq(2).html(data.research);
          $('#profile-modal .modal-icerik').eq(3).html(data.schedule);
          $('#profile-modal .modal-icerik').eq(4).html(data.notes);
          $('#profile-modal .modal-icerik').eq(5).html(data.tel);
          $('#profile-modal .modal-icerik').eq(6).html(data.email);
          $('#profile-modal .randevual-btn').attr('name',profilID);
        }
      });
    });

    $(".randevual-btn").click(function(){
      profilID = $(this).attr('name');
      $.ajax({
        url: 'get/profile/'+profilID,
        success: function(data) {
          $('#randevual-modal .modal-icerik').eq(0).html(data.name);
          $('#randevual-modal .modal-icerik').eq(1).html(data.surname);
          $('#randevual-modal .modal-icerik').eq(2).html(data.schedule);
          $('#teacher-id').attr('value',profilID);

        }
      });
    });

    $('#date-picker').datepicker({
      format: 'dd-mm-yyyy',
      weekStart: 1,
      setviewport: { month: 11, year: 2015 }
    }).on('dateChanged.bs.datepicker', function(ev){
      $('#date-picker').datepicker('hide');
    });

    var hours = $('<select>').attr('name','hour');
    for(i=0; i<8; i++){
      var hour = $('<option>').attr('value',(i+9)).text((i+9));
      hours.append(hour);
    }
    $('#hour-select').append(hours);

    var minutes = $('<select>').attr('name','minute');
    for(i=0; i<6; i++){
      var minute = $('<option>').attr('value',(i*10)).text((i*10));
      minutes.append(minute);
    }
    $('#minute-select').append(minutes);


});
