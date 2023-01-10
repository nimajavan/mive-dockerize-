FROM python:3.10.8-slim-buster

WORKDIR /usr/src/app

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN apt-get update && apt-get install -y build-essential libpq-dev
RUN rm -rf /var/lib/apt/lists/*

COPY . .

RUN pip install --upgrade pip && pip install -r requirements.txt

# COPY ./entrypoint.prod.sh .
# RUN sed -i 's/\r$//g'  entrypoint.prod.sh
# RUN chmod +x  entrypoint.prod.sh

# ENTRYPOINT ["/usr/src/app/entrypoint.prod.sh"]