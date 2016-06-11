#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip python-dev build-essential 
sudo -H pip install --upgrade pip
sudo -H pip install jupyter
sudo -H pip install pandas
pip install --user python-twitter

jupyter notebook --notebook-dir=/vagrant/notebook --no-browser --ip=0.0.0.0 &