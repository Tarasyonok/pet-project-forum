FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y \
    netcat-traditional \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN pip install --no-cache-dir poetry

COPY pyproject.toml poetry.lock /app/

RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . /app/

RUN chmod +x /app/docker-entrypoint.sh

RUN mkdir -p /app/staticfiles

ENTRYPOINT ["/app/docker-entrypoint.sh"]

CMD ["gunicorn", "-c", "gunicorn.conf.py", "django_forum.django_forum.wsgi:application"]