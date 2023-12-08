FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /book-service

COPY ./requirements.txt /book-service/
RUN pip install --no-cache-dir -r /book-service/requirements.txt

COPY ./app /book-service/app
COPY ./alembic /book-service/alembic
COPY ./alembic.ini /book-service/alembic.ini


EXPOSE PORT

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port ${PORT}"]
