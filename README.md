# Django dockerize (NGINX, CELERY, POSTGRESQL, DJANGO, REDIS, REST api)

use linux (ubuntu or debian)

step 1:

> install docker

> install docker-compose

step 2:

build and up docker compose with this command:

> sudo docker-compose -f docker-compose.yml up -d --build

step 3:

create django admin user with run this command in the root of project:

> docker-compose -f docker-compose.yaml exec web python manage.py createsuperuser

# at the end all steps are executed automatically and project run on localhost:80
