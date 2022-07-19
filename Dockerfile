# pull official base image
FROM python:3.9

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


RUN apt-get update && apt-get -y install curl
RUN apt-get update && apt-get -y install cron
RUN apt-get update && apt-get -y install nano
RUN mkdir -p /var/www/app

WORKDIR /var/www/app


# install psycopg2 dependencies
#RUN apt update \
#    && apt install python-psycopg2

# install dependencies
RUN pip install --upgrade pip
COPY requirements.txt .
RUN pip install -r requirements.txt

#RUN sed -i 's/\r$//g' /usr/src/app/docker-entrypoint.sh

# copy project
COPY . /var/www/app
# copy docker-entrypoint.sh

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh
CMD ["sh /docker-entrypoint.sh"]
