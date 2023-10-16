FROM python:3.11.2-alpine

WORKDIR /api_with_restrictions

RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py collectstatic

