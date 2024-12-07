#!/bin/bash

# Change to Project root directory.
cd /home/ec2-user/devops

#Install Nginx
sudo yum install nginx

# Install Gunicorn
pip3 install gunicorn

#Install bcrypt
pip install bcrypt

#Install Flask
pip3 install Flask

#Install Boto3
pip3 install boto3