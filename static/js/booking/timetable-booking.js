var day_booking = null;
var aud_id_booking = null;

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
    let day = event.relatedTarget.id.split(';')[0].split('=')[1];
    let aud_id = event.relatedTarget.id.split(';')[1].split('=')[1];
    day = parseDate(day);
    console.log(event.relatedTarget.id);
    console.log(day, typeof(day), day.getDate(), day.getMonth(), day.getFullYear());
    console.log(aud_id);
    day_booking = day;
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
    if (day_booking != null) {
        date = day_booking;
    }
    let date_day = date.getDate();
    let date_month = date.getMonth();
    let date_year = date.getFullYear();
    if (aud_id_booking != null) {
        aud = aud_id_booking;
    }
    console.log(name, type, start_time, end_time, amount, info, aud);
    $.ajax({
        url: '/api/v0/booking-create/',
        type: 'POST',
        data: {
            'name': name,
            'type': type,
            'amount_people': amount,
            'date': date_day + '-' + date_month + '-' + date_year,
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


let parseDate = (dateString)=> {
      const parts = dateString.split(" ");

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

      const milliseconds = Date.parse(`${year}-${month + 1}-${day}`);
      const date = new Date(milliseconds);

      return date;
}