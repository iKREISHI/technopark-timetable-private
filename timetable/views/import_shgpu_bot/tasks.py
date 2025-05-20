from .importing import import_schedule
from technoparkTimetable.celery_app import app as celery_app
import datetime
from users.models import User


@celery_app.task
def import_schedule_from_shspu_bot():
    # Получаем текущую дату
    today = datetime.date.today()

    # Получаем номер дня недели (1 - понедельник, 7 - воскресенье)
    weekday = today.weekday()

    # Вычисляем начало недели (понедельник)
    start_of_week = today - datetime.timedelta(days=weekday)

    # Вычисляем конец недели (воскресенье)
    end_of_week = start_of_week + datetime.timedelta(days=6)

    print("Начало недели:", start_of_week)
    print("Конец недели:", end_of_week)

    importing = import_schedule
    # Указываем имя пользователя, email и пароль
    username = 'auto-import-bot'
    email = 'auto-import-bot@mail.ru'
    password = 'TestPass123'

    user = None

    # Проверяем, существует ли пользователь с таким именем
    if not User.objects.filter(username=username).exists():
        # Создаем нового пользователя, если он не существует
        user = User.objects.create_user(username=username, email=email, password=password)
        print("Пользователь создан:", user.username)
    else:
        print("Пользователь уже существует")
        user = User.objects.filter(username=username)

    importing.importing(importing, start_week=start_of_week, end_week=end_of_week, user=user)
