import logging
from datetime import date, timedelta, datetime
from string import Template

from django.views import View
from django.shortcuts import redirect
from django.contrib.auth.mixins import PermissionDenied, LoginRequiredMixin
from django.urls import reverse
from django.db import IntegrityError, transaction

from users.models.university import Auditorium
from timetable.models.timetable import TimetableItem, Type_TimetableItem
from timetable.views.import_shgpu_bot.config import DATABASE_PG, USER_PG, PASSWORD_PG, HOST_PG, PORT_PG
from timetable.views.import_shgpu_bot.connect import get_connection, get_cursor, execute_sql, close_connection


class ImportSchedule:
    query_get_schedule_by_date = Template(
        '''
        select
            p.text,
            p.date,
            p.num,
            g.name        as group_name,
            a.name        as audience_name
        from pairs p
            inner join groupsofpairs gop
                on p.id = gop.pair_id
            inner join "groups" g
                on g.id = gop.group_id
            inner join audiencesofpairs aop
                on p.id = aop.pair_id
            inner join audiences a
                on a.id = aop.audience_id
        where p.date = '$date'
        order by p.num asc;
        '''
    )

    time_pair = {
        1: '08:00:00-09:30:00',
        2: '09:40:00-11:10:00',
        3: '11:20:00-12:50:00',
        4: '13:20:00-14:50:00',
        5: '15:00:00-16:30:00',
        6: '16:40:00-18:10:00',
    }

    def __init__(self):
        # один раз получаем/создаём тип "Учебное занятие"
        self.lesson_type, _ = Type_TimetableItem.objects.get_or_create(
            name="Учебное занятие"
        )

    def importing(self, start_week: date, end_week: date, user):
        conn = ""
        cursor = ""
        try:
            conn = get_connection(
                db=DATABASE_PG,
                user=USER_PG,
                password=PASSWORD_PG,
                host=HOST_PG,
                port=PORT_PG,
            )
        except Exception as e:
            logging.error(f"Connection error: {e}")
            return

        logging.debug(f"Success connect to database: {DATABASE_PG}")
        print(f"Success connect to database: {DATABASE_PG}")

        try:
            cursor = get_cursor(conn)
        except Exception as e:
            logging.error(f"Cursor error: {e}")
            close_connection(conn)
            return

        day = start_week

        while day <= end_week:
            str_day = date.strftime(day, "%Y-%m-%d")
            print(str_day)

            try:
                result = execute_sql(
                    self.query_get_schedule_by_date.substitute(date=str_day),
                    cursor,
                    all=True,
                )
            except Exception as e:
                logging.error(f"SQL error for date {str_day}: {e}")
                day = day + timedelta(days=1)
                continue

            # ключ: (clean_name, date, start_time, end_time, auditorium_id)
            grouped_pairs = {}

            for res in result:
                # res: (text, date, num, group_name, audience_name)
                text = res[0]
                pair_date = res[1]
                pair_num = res[2]
                group_name = res[3]
                audience_name = res[4]

                if text == 'день самостоятельной работы' or text == 'День самостоятельной / работы':
                    continue

                print(res)

                try:
                    auditorium = Auditorium.objects.get(name__iexact=audience_name)
                except Auditorium.DoesNotExist:
                    print(f"error!: аудитория не найдена в БД: {audience_name}")
                    print(res)
                    continue
                except Exception as e:
                    print(f"error!: {e}")
                    print(res)
                    continue

                clean_name = text.replace("/ ", "")
                start_time, end_time = self.time_pair[pair_num].split("-")

                key = (clean_name, day, start_time, end_time, auditorium.id)

                if key not in grouped_pairs:
                    grouped_pairs[key] = {
                        "clean_name": clean_name,
                        "date": day,
                        "start_time": start_time,
                        "end_time": end_time,
                        "auditorium": auditorium,
                        "groups": set(),
                    }

                grouped_pairs[key]["groups"].add(group_name)

            # запись сгруппированных данных в БД
            for key, entry in grouped_pairs.items():
                clean_name = entry["clean_name"]
                date_val = entry["date"]
                start_time = entry["start_time"]
                end_time = entry["end_time"]
                auditorium = entry["auditorium"]
                groups_set = entry["groups"]

                # формируем info: "… | группы A, B, C"
                base_info = " ".join([s for s in clean_name.split()[2:]])
                groups_str = ", ".join(sorted(groups_set)) if groups_set else ""
                if groups_str:
                    info = f"{base_info} | группы {groups_str}"
                else:
                    info = base_info

                lookup_fields = dict(
                    name=clean_name,
                    start_time=start_time,
                    end_time=end_time,
                    date=date_val,
                )

                with transaction.atomic():
                    # ищем все записи с тем же name/date/time и этой аудиторией
                    qs = (
                        TimetableItem.objects
                        .filter(**lookup_fields)
                        .filter(auditorium__id=auditorium.id)
                        .distinct()
                    )

                    obj = None
                    if qs.exists():
                        obj = qs.first()
                        # если дублей несколько — остальные удаляем
                        extra = qs.exclude(pk=obj.pk)
                        if extra.exists():
                            print(
                                f"Удаляю дубликаты для {clean_name} "
                                f"{date_val} {start_time}-{end_time} аудитория {auditorium.name}: "
                                f"{list(extra.values_list('id', flat=True))}"
                            )
                            extra.delete()

                        # обновляем найденный объект
                        obj.type = self.lesson_type
                        obj.organazer = user
                        obj.amount_people = 25
                        obj.info = info
                        obj.status = "APPROVED"
                        obj.who_approved = user
                        obj.datetime_approved = datetime.now()
                        obj.save()
                    else:
                        # создаём новый объект
                        obj = TimetableItem.objects.create(
                            type=self.lesson_type,
                            organazer=user,
                            amount_people=25,
                            info=info,
                            status="APPROVED",
                            who_approved=user,
                            datetime_approved=datetime.now(),
                            **lookup_fields,
                        )

                    # выставляем аудиторию (одна аудитория на запись)
                    obj.auditorium.set([auditorium])

                    print(
                        f"Запись расписания: id={obj.id}, "
                        f"{clean_name}, {date_val} {start_time}-{end_time}, аудитория {auditorium.name}"
                    )

            day = day + timedelta(days=1)

        close_connection(conn)


class ImportScheduleView(LoginRequiredMixin, View):
    def get(self, request, monday: str, sunday: str):
        if not request.user.is_superuser:
            raise PermissionDenied

        print(f"monday - {monday}, sunday - {sunday}")
        mon = datetime.strptime(monday, '%d_%m_%y').date()
        sun = datetime.strptime(sunday, '%d_%m_%y').date()

        importer = ImportSchedule()
        importer.importing(start_week=mon, end_week=sun, user=request.user)

        return redirect(reverse("schedule", args=[monday, sunday]))

    def post(self, request):
        # если POST не нужен — можно оставить как есть
        return redirect(reverse("schedule", args=[]))
