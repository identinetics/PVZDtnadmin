#!/usr/bin/env bash


ssh devl11 -c /home/r2h2/devl/docker/c-pvzdweb-pg-dev/reset_pg_data.sh
manage.py createsuperuser --email rainer@hoerbe.at
manage.py migrate
./load_testdata.sh