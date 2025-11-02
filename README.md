# Проект Service Desk
Проект представляет собой backend-приложение написанное на Python с использованием 
брокера сообщений RabbitMQ и БД PostgreSQL

## Как запустить проект:
* Склонировать текущий репозиторий: ```git clone git@github.com:topclassprogrammer/service_desk.git```
* Перейти в папку проекта: ```cd service_desk```
* Запустить контейнеры: ```docker-compose up -d```
* Чтобы открыть веб-интерфейс RabbitMQ необходимо перейти по адресу http://localhost:15672 и 
аутентифицироваться под заданными переменными окружения 
RABBITMQ_DEFAULT_USER и RABBITMQ_DEFAULT_PASS указанными в файле .env
