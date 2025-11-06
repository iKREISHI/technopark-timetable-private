.PHONY: backup

build:
	docker build .
	docker-compose up -d --build
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
#	docker-compose exec web python manage.py loaddata users_data.json
#	docker-compose exec web python manage.py loaddata timetable_data.json
	#docker-compose exec web ./backup_script.sh
#	docker-compose exec web cron -f &&
#	docker-compose exec web python manage.py runcrons
#	docker-compose exec web python manage.py dbbackup

stop:
	docker-compose stop

start:
	docker-compose up -d
#	docker-compose exec web cron -f

restart:
	docker-compose restart
#	docker-compose exec web cron -f &&

psql:
	docker-compose exec db psql --username=root_timetable --dbname=timetableDB

rebuild-web:
	docker build .

rebuild-compose:
	docker-compose up -d --build
	docker-compose exec web python manage.py makemigrations
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata users_data.json
	docker-compose exec web python manage.py loaddata timetable_data.json
	docker-compose exec web ./backup_script.sh
# ./manage.py loaddata --exclude auth.permission --exclude contenttypes
#	docker-compose exec web cron -f
#	docker-compose exec web python manage.py runcrons
#	docker-compose exec web python manage.py dbbackup

backup:
	docker-compose exec web ./backup_script.sh

dev: dev-containers migrate

migrate:
	venv/bin/python manage.py makemigrations
	venv/bin/python manage.py migrate

load-data:
	venv/bin/python manage.py loaddata users_data.json
	venv/bin/python manage.py loaddata timetable_data.json

dev-containers:
	docker-compose up db -d
	# docker-compose up nginx -d
	docker-compose up rabbitmq -d