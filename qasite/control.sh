#!/usr/bin/env bash

PYTHON_CMD=`type -P python3.6`
cd /home/project/qasite.s.news/qasite

umask 0002

${PYTHON_CMD} manage.py makemigrations 
${PYTHON_CMD} manage.py migrate
${PYTHON_CMD} manage.py collectstatic --noinput
