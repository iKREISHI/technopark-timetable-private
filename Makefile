
build:
	docker build .
	docker-compose up -d --build
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata users_data.json
	docker-compose exec web python manage.py loaddata timetable_data.json
	docker-compose exec web python manage.py runcrons
	docker-compose exec web python manage.py dbbackup

stop:
	docker-compose stop

start:
	docker-compose up -d

restart:
	docker-compose restart

psql:
	docker-compose exec db psql --username=root_timetable --dbname=timetableDB

rebuild-web:
	docker build .

rebuild-compose:
	docker-compose up -d --build
	docker-compose exec web python manage.py migrate
	docker-compose exec web python manage.py loaddata users_data.json
	docker-compose exec web python manage.py loaddata timetable_data.json