#!/bin/bash

# Stop any existing Flask app running on the EC2 instance. 
sudo pkill -f "flask run"

#Stopping Gunicorn server.
sudo pkill -f "gunicorn"
