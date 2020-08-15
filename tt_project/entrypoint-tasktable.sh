#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $SQL_HOST $SQL_PORT; do
        sleep 0.1
    done

    echo "PostgreSQL started"
fi

echo "Waiting for rabbit..."

while ! nc -z $RABBIT_HOST $RABBIT_PORT; do
    sleep 0.1
done

echo "RabbitMQ started"

echo "Waiting for redis..."

while ! nc -z $REDIS_HOST $REDIS_PORT; do
    sleep 0.1
done

echo "Redis started"

python3 manage.py makemigrations
python3 manage.py migrate

exec "$@"
