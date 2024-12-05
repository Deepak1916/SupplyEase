#!/bin/bash
# Stop any existing Flask app running on the EC2 instance.
#echo "Stopping existing Flask server..."
sudo pkill -f "flask run"
#Stopping Gunicorn server.
sudo pkill -f "gunicorn"
