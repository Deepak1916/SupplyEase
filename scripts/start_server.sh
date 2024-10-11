#!/bin/bash
cd /home/ec2-user/devops
export FLASK_APP=app.py
export FLASK_ENV=development
flask run --host=0.0.0.0 --port=5000
#gunicorn -w 3 -b 0.0.0.0:5000 app:app --daemon