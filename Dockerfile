FROM python:3.9

RUN mkdir /usr/crm

WORKDIR /usr/crm
COPY backend/req.txt /usr/crm

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip

RUN pip install -r req.txt

COPY backend /usr/crm
