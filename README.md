# Выпускная квалификационная работа на тему: "Разработка веб-системы бронирования и генерации расписания Технопарка УПК" 
## Выполнена с использованием ЯП Python, Django, PostgreSQL

### Для запуска dev выполните команды:
```bash
python -m venv venv
source venv/bin/activate
cd docker/database/TimeTableDB/ && docker-compose up
cp -f .env.dev.sample .env
mkdir backups 
python manage.py makemigrations 
python manage.py migrate 
python manage.py runserver
```
### Для сборки и запуска проекта в docker используйте:
```bash
cp -f .env.prod.sample .env.prod
make build
```
## SSL HTTPS
### Для получения сертификата
```bash
docker compose run --rm  certbot certonly --webroot --webroot-path /var/www/certbot/ -d tpbook2.shspu.ru  
```
### Обновление сертификата
```bash
docker compose run --rm certbot renew
```