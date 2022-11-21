FROM python:3.10-alpine as builder

WORKDIR /usr/src/movies_db

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev

RUN pip install --upgrade pip\
    && pip install flake8==3.9.2
COPY . .
RUN flake8 --ignore=E501,F401

COPY ./requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /usr/src/movies_db/wheels -r requirements.txt


FROM python:3.10-alpine

RUN mkdir -p /home/movies_db

RUN addgroup -S movies_db && adduser -S movies_db -G movies_db

ENV HOME=/home/movies_db \
    APP_HOME=/home/movies_db/etl
RUN mkdir $APP_HOME
WORKDIR $APP_HOME

RUN apk update && apk add libpq
COPY --from=builder /usr/src/movies_db/wheels /wheels
COPY --from=builder /usr/src/movies_db/requirements.txt .
RUN pip install --no-cache /wheels/*

COPY ./etl/entrypoint.sh .
RUN sed -i "s/\r$//g"  $APP_HOME/entrypoint.sh \
    && chmod +x  $APP_HOME/entrypoint.sh

COPY ../postgres_to_es $APP_HOME

RUN chown -R movies_db:movies_db $APP_HOME

USER movies_db

ENTRYPOINT ["/home/movies_db/etl/entrypoint.sh"]