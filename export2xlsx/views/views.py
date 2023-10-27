from django.http import HttpResponse, Http404
from django.views import View
from django.shortcuts import get_object_or_404
from wsgiref.util import FileWrapper
import mimetypes
import os
from django.conf import settings
from export2xlsx.converter.converter import json_to_excel


class ExcelDownloadWeekView(View):

    def get(self, request, monday: str, sunday: str, university_id: int, *args, **kwargs):
        # Получите полный путь к файлу на сервере
        domain = request.META['HTTP_HOST']
        json_couples = f"http://{domain}/api/v0/get-booking-week/{university_id}/{monday}-{sunday}/?format=json"
        json_list = f"http://{domain}/api/v0/get-auditoriums/{university_id}/?format=json"
        # json_couples = f"http://tpbook2.shgpi/api/v0/get-booking-week/{university_id}/{monday}-{sunday}/?format=json"
        # json_list = f"http://tpbook2.shgpi/api/v0/get-auditoriums/?format=json"
        file_path = json_to_excel(
            json_couples=json_couples,
            json_list=json_list
        )

        # Проверьте существование файла
        if not os.path.exists(file_path):
            raise Http404("File does not exist")

        # Откройте файл для чтения в бинарном режиме
        with open(file_path, 'rb') as file:
            # Определите MIME-тип файла
            content_type, encoding = mimetypes.guess_type(file_path)
            content_type = content_type or 'application/octet-stream'

            # Создайте HTTP-ответ с файлом в виде прикрепленного содержимого
            response = HttpResponse(FileWrapper(file), content_type=content_type)
            response['Content-Disposition'] = f'attachment; filename={os.path.basename(f"Technopark_schedule-{monday}-{sunday}.xlsx")}'
            response['Content-Length'] = os.path.getsize(file_path)

            # Удалите файл после отправки
            os.remove(file_path)

            return response
