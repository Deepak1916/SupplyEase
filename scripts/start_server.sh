#!/bin/bash
cd /home/ec2-user/devops
# export FLASK_APP=app.py
# export FLASK_ENV=development
#/usr/bin/python3 -m flask run --host=0.0.0.0 --port=5000
/usr/bin/python3 -m gunicorn -b 0.0.0.0:5000 app:app --daemon