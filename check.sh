#!/bin/bash

default_endpoint="http://tpbook2.shgpi/api/v0/"
endpoint=${1:-$default_endpoint}

response=$(curl -s -o /dev/null -w "%{http_code}" $endpoint)

if [ $response -eq 200 ]; then
  echo "Endpoint $endpoint доступен. Все в порядке!"
else
  echo "Ошибка: Не удалось подключиться к $endpoint. Код ответа: $response"
fi
