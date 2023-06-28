# syntax=docker/dockerfile:1

FROM node:16
WORKDIR /frontend
RUN npm install -g @quasar/cli
COPY package.json ./
RUN yarn install

COPY . .
