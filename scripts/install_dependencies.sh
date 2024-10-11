#!/bin/bash
cd /home/ec2-user/devops
#sudo yum install python3 python3-pip -y
#Install Nginx
sudo yum install nginx
# Install Gunicorn
pip3 install gunicorn

#Install Flask
pip3 install Flask
#pip3 install -r requirement.txt