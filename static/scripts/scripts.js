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

    var profilID;
    $(".profile-btn").click(function(){
      profilID = $(this).attr("name");
      $.ajax({
        url: 'get/profile/'+profilID,
        success: function(data) {
          $('#profile-modal .modal-icerik').eq(0).html(data.name);
          $('#profile-modal .modal-icerik').eq(1).html(data.surname);
          $('#profile-modal .modal-icerik').eq(2).html(data.email);
        }
      });
    });

    $('#date-picker').datepicker({
      format: 'mm-dd-yyyy',
      weekStart: 1,
      setviewport: { month: 11, year: 2015 }
    }).on('dateChanged.bs.datepicker', function(ev){
      $('#date-picker').datepicker('hide');
    });

    var hours = $('<select>').attr('name','hour');
    for(i=0; i<8; i++){
      var hour = $('<option>').attr('value',(i+9)+':00').text((i+9)+':00');
      hours.append(hour);
    }
    $('#hour-select').append(hours);

    /*
        var weekTable = $('<table>').addClass('week-table');
        var gunler = ['Pazartesi', 'Salı', 'Çarşamba', 'Perşembe', 'Cuma']
        var row = $('<tr>').addClass('days').addClass('row');
        var col = $('<td>').addClass('col-2').text('Tarih:');
        row.append(col);
        for(i=0; i<5; i++){
          var col = $('<td>').text(gunler[i]).addClass('col-2');
          row.append(col);
          weekTable.append(row);
        }
        for(i=0; i<8; i++){
          var row = $('<tr>').addClass('row');
          var col = $('<td>').text((i+9)+':00').addClass('col-2');
          row.append(col);
          for(j=0; j<5; j++){
            var col = $('<td>').attr({row:i, col:j}).addClass('col-2');
            var check = $('<input>').attr({
                          type: 'radio',
                          name: 'date',
                          value: i+'-'+j
                        });
            col.append(check);
            row.append(col);
          }
          weekTable.append(row);
        }
        $('#here_table').append(weekTable);

    */

});
