FROM python:3.10-alpine

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apk update \
    postgresql-dev gcc python3-dev musl-dev \
    add apk add jpeg-dev zlib-dev libjpeg py3-pillow py3-wheel

RUN apk add tiff-dev jpeg-dev openjpeg-dev zlib-dev freetype-dev lcms2-dev \
    libwebp-dev tcl-dev tk-dev harfbuzz-dev fribidi-dev libimagequant-dev \
    libxcb-dev libpng-dev \

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY . .
# RUN cp ./config/DataBase.py ./config/DataBaseold.py  mv -f ./config/dockerDB.py ./config/DataBase.py


