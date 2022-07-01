# syntax=docker/dockerfile:1

FROM python:3.9
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1
WORKDIR /backend

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .