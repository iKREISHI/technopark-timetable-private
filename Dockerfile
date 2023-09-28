FROM python:3.10-slim-bookworm

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установка русской локали
RUN apt-get update && apt-get upgrade -y
RUN apt-get install -y locales
RUN sed -i 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen
RUN locale-gen
ENV LANG ru_RU.UTF-8
RUN echo 'LANG=ru_RU.UTF-8' >> /etc/default/locale
RUN ln -sf /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime
RUN echo "Asia/Yekaterinburg" > /etc/timezone

RUN apt-get install -y postgresql-client cron vim mc procps libpq-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
RUN chmod +x /usr/src/app/backup_script.sh

#RUN echo "0 0 * * * /usr/src/app/backup_script.sh" >> /etc/crontab
# RUN crontab -l | { cat; echo "0 0 * * * /usr/src/app/backup_script.sh > /proc/1/fd/1 2>/proc/1/fd/2"; } | crontab -
COPY cron_backup /etc/cron.d/cronfile
RUN chmod 0644 /etc/cron.d/cronfile && crontab /etc/cron.d/cronfile

# CMD ["cron","-f", "-L", "2"]
CMD cron -f
