#!/bin/bash

bash .sh
sudo apt-get update
sudo apt-get install python3 -y
sudo apt-get install python3-venv -y
sudo apt-get install python3-pip -y

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pytest --cov=application tests/  --cov-report html


sudo systemctl stop game-review.service
sudo systemctl daemon-reload
sudo systemctl start game-review.service