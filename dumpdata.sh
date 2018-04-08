#!/bin/bash

python manage.py dumpdata \
    --natural-foreign --natural-primary \
    -e contenttypes -e auth.Permission \
    --indent 4 \
    > database/initial_data.json
