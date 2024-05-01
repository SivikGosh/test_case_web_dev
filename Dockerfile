FROM python:3.12.2

WORKDIR /app

COPY . .

EXPOSE 8000

CMD gunicorn 'project.wsgi' --bind=0.0.0.0:8000
