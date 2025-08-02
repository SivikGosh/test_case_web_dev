FROM python:3.13

WORKDIR /project

COPY ./project/ ./
COPY ./pyproject.toml .

RUN pip install --upgrade pip
RUN pip install .

RUN python manage.py collectstatic --noinput

CMD [ "gunicorn", "core.wsgi:application", "--bind", "0.0.0.0:8000" ]
