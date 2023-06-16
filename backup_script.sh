#!/bin/bash

# Переход в директорию, где находится ваше Django-приложение
cd /usr/src/app

# Активация виртуальной среды Python (если используется)
# source /path/to/your/virtualenv/bin/activate

# Запуск команды резервного копирования базы данных Django
python manage.py dumpdata > /usr/src/app/backup/db_backup_$(date +%Y-%m-%d).json

