#!/bin/bash

# It is responsability of the deployment orchestration to execute before
# migrations, create default admin user, populate minimal data, etc.

gunicorn kpi_service.wsgi --config kpi_service/gunicorn_conf.py
