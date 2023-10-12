from django.views import View
from django.shortcuts import render, redirect
from datetime import date, timedelta, datetime
from string import Template
import locale
from users.models.university import Auditorium
from timetable.models.timetable import TimetableItem, Type_TimetableItem
from timetable.views.import_shgpu_bot.config import *
from django.contrib.auth.mixins import PermissionRequiredMixin, PermissionDenied, LoginRequiredMixin
from timetable.views.import_shgpu_bot.connect import *
from django.urls import reverse


class import_schedule:
    query_get_schedule_by_date = Template('''
                select p.text, p.date, p.num, g.name from pairs p
                inner join groupsofpairs gop on p.id = gop.pair_id
                inner join "groups" g on g.id = gop.group_id 
                where p.date = '$date' 
                order by p.num asc;
            ''')
    auditoriums = Auditorium.objects.all()
    items = TimetableItem.objects.all()
    time_pair = {
        1: '08:00:00-09:30:00',
        2: '09:40:00-11:10:00',
        3: '11:20:00-12:50:00',
        4: '13:20:00-14:50:00',
        5: '15:00:00-16:30:00',
        6: '16:40:00-18:10:00',
    }

    def __init__(self):
        pass

    def importing(self, start_week: date, end_week: date, user):
        # mon = datetime.strptime(start_week, '%d_%m_%y').date()
        # sun = datetime.strptime(end_week, '%d_%m_%y').date()
        # if item.date >= start_week and item.date <= end_week
        results = []
        conn = get_connection(
            db=DATABASE_PG, user=USER_PG, password=PASSWORD_PG,
            host=HOST_PG, port=PORT_PG
        )
        cursor = get_cursor(conn)
        day = start_week
        while day <= end_week:
            str_day = date.strftime(day, "%Y-%m-%d")
            print(str_day)
            result = execute_sql(self.query_get_schedule_by_date.substitute(date=str_day), cursor, all=True)
            for res in result:
                if res[0] == 'день самостоятельной работы' or res[0] ==  'День самостоятельной / работы':
                    continue
                # print(res)
                for aud in self.auditoriums:
                    try:
                        if res[0].split()[-1].lower() == aud.name.lower():
                            print(f'-- {res}')
                            param = {
                                "name": res[0].replace("/ ", "") + " " + res[-1],
                                "start_time": self.time_pair[res[2]].split("-")[0],
                                "end_time": self.time_pair[res[2]].split("-")[1],
                                "date": day,
                            }
                            params = {
                                # "auditorium": Auditorium.objects.filter(name=res[0].split()[-1]).first(),
                                # "auditorium": Auditorium.objects.get(name=res[0].split()[-1]),
                                "type": Type_TimetableItem.objects.get(name="Учебное занятие"),
                                "organazer": user,
                                "amount_people": 25,
                                # "start_time": self.time_pair[res[2]].split("-")[0],
                                # "end_time": self.time_pair[res[2]].split("-")[1],
                                # "date": day,
                                "info": " ".join([s for s in res[0].replace("/ ", "").split()[2:]]),
                                "status": "APPROVED",
                                'who_approved': user,
                                "datetime_approved": datetime.now(),
                            }
                            # if TimetableItem.objects.filter(start_time=params["start_time"], end_time=params["end_time"], auditorium__name=res[0].split()[-1]).first():
                            #     params["status"] = "PENDING"
                            obj, created = TimetableItem.objects.update_or_create(defaults=params, **param)
                            if created:
                                print(f'Object was created successful - {res[0].replace("/ ", "")}')
                            else:
                                print('Object was updated')
                            obj.auditorium.set([Auditorium.objects.get(name=res[0].split()[-1])])
                    except Exception as e:
                        print(f'error!: {e} | {res}')
            day = day + timedelta(days=1)
        close_connection(conn)


class ImportScheduleView(View, LoginRequiredMixin):
    def get(self, request, monday: str, sunday: str):
        if not request.user.is_superuser:
            raise PermissionDenied
        print(f'monday - {monday}, sunday - {sunday}')
        mon = datetime.strptime(monday, '%d_%m_%y').date()
        sun = datetime.strptime(sunday, '%d_%m_%y').date()
        importing = import_schedule
        importing.importing(importing, start_week=mon, end_week=sun, user=request.user)

        return redirect(reverse('schedule', args=[ monday, sunday]))

    def post(self, request):
        pass
