# syntax=docker/dockerfile:1

FROM nikolaik/python-nodejs:python3.9-nodejs16
COPY frontend/package*.json ./frontend
COPY requirements.txt .

RUN pip install -r requirements.txt
WORKDIR /frontend
RUN yarn install --production=true

COPY . .
RUN quasar build -p 9000

FROM nginx:1.22
COPY nginx/local.conf /etc/nginx/conf.d/local.conf
EXPOSE 80 9000