#!/bin/bash

python manage.py migrate

gunicorn kpi_service.wsgi --config kpi_service/gunicorn_conf.py
