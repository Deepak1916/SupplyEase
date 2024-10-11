#!/bin/bash
cd /home/ec2-user/devops
gunicorn -w 3 -b 0.0.0.0:5000 app:app --daemon