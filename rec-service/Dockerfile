FROM python:3.10

# Выбор папки, в которой будет вестись работа
WORKDIR /rec-service

COPY ./requirements.txt /rec-service/
RUN pip install --no-cache-dir -r /rec-service/requirements.txt

COPY ./app /rec-service/app

EXPOSE 81

CMD ["/bin/sh", "-c", \
    "uvicorn app.main:app --host 0.0.0.0 --port 81"]
