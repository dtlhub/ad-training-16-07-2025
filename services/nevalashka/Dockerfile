#FROM php:5.5-apache
FROM php:5.5-apache

# RUN sed -i s/deb.debian.org/archive.debian.org/g /etc/apt/sources.list
# RUN sed -i 's|security.debian.org|archive.debian.org|g' /etc/apt/sources.list 
#RUN sed -i '/stretch-updates/d' /etc/apt/sources.list

RUN echo "deb [trusted=yes] http://archive.debian.org/debian stretch main non-free contrib" > /etc/apt/sources.list
RUN echo "deb-src [trusted=yes] http://archive.debian.org/debian stretch main non-free contrib" >> /etc/apt/sources.list

RUN echo "deb [trusted=yes] http://archive.debian.org/debian-security stretch/updates main non-free contrib" >> /etc/apt/sources.list

RUN apt-get update && apt-get install -y zlib1g-dev libicu-dev g++ libmcrypt-dev php-mysqli mysql-client

RUN apt-get update \
    &&  docker-php-ext-install mbstring pdo_mysql mcrypt mysqli

USER root

COPY src/ /var/www/html/

RUN usermod -u 1001 www-data

COPY docker-php-entrypoint /usr/local/bin/
