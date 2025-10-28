# Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV POETRY_VIRTUALENVS_CREATE=false

WORKDIR /app

# system deps for mysqlclient / pillow etc
RUN apt-get update \
 && apt-get install -y --no-install-recommends build-essential gcc libmariadb-dev-compat libmariadb-dev libpq-dev curl netcat ca-certificates \
 && rm -rf /var/lib/apt/lists/*

# copy requirements first for caching
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# copy project
COPY . /app

# make entrypoint executable
COPY docker-entrypoint.sh /usr/local/bin/
RUN chmod +x /usr/local/bin/docker-entrypoint.sh

# create static dir
RUN mkdir -p /vol/web/staticfiles /vol/web/media

ENV STATIC_ROOT=/vol/web/staticfiles
ENV MEDIA_ROOT=/vol/web/media

EXPOSE 8000

ENTRYPOINT ["docker-entrypoint.sh"]
CMD ["gunicorn", "JELAYAN_CAPITAL.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "3", "--log-level", "info"]
