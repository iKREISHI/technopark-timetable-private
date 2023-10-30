var day_booking = null;
var aud_id_booking = null;
var Day, Month, Year = null;

$('#infoBookingModal').on('show.bs.modal', (event) => {
    let item_id = event.relatedTarget.id.split('=')[1];
    //console.log(id);
    //$('.modal-body').text(item_id);
    getTimetableItemBaseInfo(item_id);
});

$('#infoBookingModal').on('hide.bs.modal', (event) => {
    $('#modal-output').empty();
});


function getTimetableItemBaseInfo(id) {
      $.ajax({
            url: '/api/v0/timetable-item-info/' + id + '/',
            type: 'GET',
            success: (response) => {
                  console.log(response);
                  let out = $('#modal-output');
                  out.empty();
                  out.append('<h2 style="text-align: center">Название: '+ response.name +'</h2>');
                  out.append('<p>Дата: '+ response.date +'</p>');
                  out.append('<p>Время начала: '+ response.start_time +'</p>');
                  out.append('<p>Время окончания: '+ response.end_time +'</p>');
                  $.each(response.auditorium, (index, auditorium) => {
                      out.append('<p>Аудитория: '+ auditorium.name +'</p>')
                  });
                  if (response.organazer.first_name == "" && response.organazer.last_name == "")
                      out.append('<p>Ответственный: ' + response.organazer.username + '</p>');
                  else {
                      out.append('<p>Ответственный: '
                      + response.organazer.first_name + ' '
                      + response.organazer.last_name + ' '
                      + response.organazer.patronymic
                      +'</p>');
                  }
            },
            error: (textStatus, error) => {
                console.log(textStatus)
                console.log(error);
                $('#modal-output').append('<h2>Вознила ошибка</h2>')
            }
      });
}

$('#BookingFormModal').on('show.bs.modal', (event) => {
    console.log(event);
    let day = event.relatedTarget.id.split(';')[0].split('=')[1];
    let aud_id = event.relatedTarget.id.split(';')[1].split('=')[1];
    getDateStr(day);
    //day.month -= 1;
    console.log(event.relatedTarget.id);
    console.log(aud_id);
    aud_id_booking = aud_id;
    $('#modal-form-booking')[0].reset();

});

$('#modal-form-booking').submit((event) => {
    event.preventDefault();
    let name = $('#id_name').val();
    let type = $("#id_type").val();
    let start_time = $('#id_start_time').val();
    let end_time  = $('#id_end_time').val();
    let amount = $('#id_amount_people').val();
    let info = $('#id_info').val();
    let date = null;
    let aud = null;
    if (aud_id_booking != null) {
        aud = aud_id_booking;
    }
    console.log(name, type, start_time, end_time, amount, info, aud);
    console.log('-----------------');
    console.log(Day + '-' + Month + '-' + Year);
    $.ajax({
        url: '/api/v0/booking-create/',
        type: 'POST',
        data: {
            'name': name,
            'type': type,
            'amount_people': amount,
            'date': Year + '-' + Month + '-' + Day,
            'start_time': start_time,
            'end_time': end_time,
            'auditorium': aud,
            'info': info,
            'organazer': '',
        },
        beforeSend: function(xhr, settings) {
            xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
        },
        success: (response, error) => {
            console.log(response);
            console.log(error);
            $('#modal-form-booking')[0].reset();
            console.log('Success! booking form hide');
            location.reload();
        },
        error: (error, response) => {
            console.log(error);
            console.log(response);
            console.log(error.responseJSON[0]);
            $('.alert-danger').text(error.responseJSON[0]).removeClass('d-none');
        }
    });
});

$('#BookingFormModal').on('hide.bs.modal', (event) => {
    console.log('booking form hide');
    //$('#modal-output').empty();
    $('.alert-danger').addClass('d-none');
    $('#modal-form-booking')[0].reset();
});

let getCookie = (name) => {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
      let cookies = document.cookie.split(';');
      for (let i = 0; i < cookies.length; i++) {
        let cookie = cookies[i].trim();
        if (cookie.substring(0, name.length + 1) === (name + '=')) {
          cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
          break;
        }
      }
    }
    return cookieValue;
}

function getDateStr(dateStr) {
    const parts = dateStr.split(" ");
    const months = {
            "января": 1,
            "февраля": 2,
            "марта": 3,
            "апреля": 4,
            "мая": 5,
            "июня": 6,
            "июля": 7,
            "августа": 8,
            "сентября": 9,
            "октября": 10,
            "ноября": 11,
            "декабря": 12
      };

      const day = parseInt(parts[0], 10);
      const month = months[parts[1]];
      const year = parseInt(parts[2], 10);
      Day = day; Month = month; Year = year;
}