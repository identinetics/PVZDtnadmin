# NGINX proxy

maps PVZDweb + SigProxy into single service

Prod: handled in the docker project

MacOS/Dev:
Docroot is: /usr/local/var/www

The default port has been set in /usr/local/etc/nginx/nginx.conf to 8080 so that
nginx can run without sudo.

nginx will load all files in /usr/local/etc/nginx/servers/.

Or, if you don't want/need a background service you can just run:
  nginx



