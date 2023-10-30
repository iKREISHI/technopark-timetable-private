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
                  out.append('<p>Тип: '+ response.type.name +'</p>');
                  out.append('<p>Дата: '+ response.date +'</p>');
                  out.append('<p>Время начала: '+ response.start_time +'</p>');
                  out.append('<p>Время окончания: '+ response.end_time +'</p>');
                  out.append('<p>Количество человек: ' + response.amount_people + '</p>');
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
                  out.append('<p>Дополнительная информация: '+ response.info +'</p>');
            },
            error: (textStatus, error) => {
                console.log(textStatus)
                console.log(error);
                $('#modal-output').append('<h2>Вознила ошибка</h2>')
            }
      });
}