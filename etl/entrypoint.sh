#!/bin/sh

if [ "$DB_NAME" = "movies_database" ]
then
    echo "Launch movies database."

    while ! nc -z "$DB_HOST" "$DB_PORT"; do
      sleep 0.1
    done

    echo "Movies database launced"
fi

exec "$@"