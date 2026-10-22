ARG PHP_IMAGE=php:8.4.27-apache-bookworm@sha256:e653ff90d7f6e2e6f81eddb07c864f1eae224ccbf5143f82a44f25e2f110e320
FROM ${PHP_IMAGE}
ARG PHP_BASE_DIGEST
ENV APACHE_RUN_USER=labphp APACHE_RUN_GROUP=labphp APACHE_PID_FILE=/tmp/apache.pid APACHE_RUN_DIR=/tmp/apache APACHE_LOCK_DIR=/tmp/apache PHP_BASE_DIGEST=${PHP_BASE_DIGEST}
RUN groupadd -g 10001 labphp && useradd -u 10001 -g 10001 -s /usr/sbin/nologin labphp \
 && sed -i 's/Listen 80/Listen 8080/' /etc/apache2/ports.conf \
 && sed -i 's/:80>/:8080>/' /etc/apache2/sites-available/000-default.conf \
 && mkdir -p /php-data && chown 10001:10001 /php-data
COPY php/lab.conf /etc/apache2/conf-enabled/lab.conf
COPY php/lab.ini /usr/local/etc/php/conf.d/lab.ini
COPY php/index.php /var/www/html/index.php
USER 10001:10001
EXPOSE 8080
CMD ["apache2-foreground"]
