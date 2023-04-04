# syntax=docker/dockerfile:1
FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /POSTREAL
COPY . .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
#COPY post_real .env Dockerfile manage.py /POSTREAL/