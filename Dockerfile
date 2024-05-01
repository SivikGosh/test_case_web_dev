FROM python:3.12.2-slim

WORKDIR /app

COPY . .

RUN pip install -r requirements.txt

EXPOSE 8000

CMD gunicorn 'project.wsgi' --bind=0.0.0.0:8000
