FROM python:3.9-buster as builder

WORKDIR /app

COPY . .

EXPOSE 8000

RUN pip install -r requirements.txt

CMD ["gunicorn src.main:app -w 3 -b :8000 -k uvicorn.workers.UvicornWorker"]