FROM python:3.8

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /code

COPY requirements.txt .
COPY instruments_data.json .
RUN pip install -r requirements.txt

COPY . .

