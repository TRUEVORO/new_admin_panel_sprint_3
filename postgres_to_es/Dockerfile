FROM python:3.11.2-slim-buster as build

WORKDIR /opt/postgres_to_es

COPY ./requirements.txt .

RUN apt update \
    && apt install -y gcc libpq-dev \
    && python -m venv venv \
    && venv/bin/pip install --no-cache-dir --upgrade pip \
    && venv/bin/pip install --no-cache-dir -r requirements.txt

FROM python:3.11.2-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/postgres_to_es/venv/bin:${PATH}"

ARG APP=/opt/postgres_to_es
ARG USER=web

WORKDIR ${APP}

RUN apt update \
    && apt install -y --no-install-recommends  \
      curl \
      libpq-dev \
      netcat \
    && rm -rf /var/lib/apt/lists/* \
    && groupadd -r ${USER} \
    && useradd -d ${APP} -r -g ${USER} ${USER}

COPY --chown=${USER}:${USER} --from=build ${APP}/venv ./venv
COPY --chown=${USER}:${USER} . .

RUN chmod +x ${APP}/entrypoint.sh \
    && chmod -R +r ${APP}/elasticsearch_indexes

USER ${USER}

ENTRYPOINT ["/opt/postgres_to_es/entrypoint.sh"]
