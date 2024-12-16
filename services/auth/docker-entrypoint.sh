#!/bin/bash

# =================================================== #
#       Команды для первого "холодного" запуска       #
#       Вводить один раз вручную в контейнере         #
# =================================================== #

# alembic upgrade head

# python create_roles.py

# python create_superuser.py $AUTH_SUPERUSER_USERNAME $AUTH_SUPERUSER_PASSWORD

PORT=${AUTH_SERVICE_PORT:-8001}

exec gunicorn -k uvicorn.workers.UvicornWorker -w 4 -b 0.0.0.0:${PORT} main:app