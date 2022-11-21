#!/bin/sh

if [ "$DB_NAME" = "postgres" ]
then
    echo "Launch movies database."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "Movies database launched"
fi

python main.py

exec "$@"