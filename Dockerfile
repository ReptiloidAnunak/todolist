FROM python:3.10-slim

WORKDIR /todolist
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY todolist .
COPY core .
COPY media .
COPY manage.py .
COPY poetry.lock .
COPY pyproject.toml .
COPY README.md .
CMD todolist run -h 0.0.0.0 -p 80

