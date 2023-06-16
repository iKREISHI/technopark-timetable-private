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

RUN apt-get install -y postgresql-client vim mc

#RUN apk add --no-cache tzdata
#RUN cp /usr/share/zoneinfo/Asia/Yekaterinburg /etc/localtime
#ENV LANG ru_RU.UTF-8
#RUN apk add --no-cache ttf-dejavu musl-locales musl-locales-lang
#
#RUN apk update && apk add postgresql-dev postgresql-client gcc python3-dev py3-setuptools musl-dev \
#    jpeg-dev zlib-dev libjpeg py3-pillow py3-wheel \
#    tiff-dev openjpeg-dev freetype-dev lcms2-dev \
#    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
#    libxcb-dev libpng-dev

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# RUN cp ./config/DataBase.py ./config/DataBaseold.py  mv -f ./config/dockerDB.py ./config/DataBase.py


