FROM python:3.10-slim

WORKDIR /todolist
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY todolist .
COPY core .
COPY manage.py .
COPY poetry.lock .
COPY pyproject.toml .
CMD python manage.py runserver 0.0.0.0:8000

