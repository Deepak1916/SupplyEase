#!/bin/bash

#Chaning to project root directory
cd /home/ec2-user/devops

# Running application using Gunicorn in background using Daemon mode.
/usr/bin/python3 -m  gunicorn -b 0.0.0.0:5000 app:app --daemon
