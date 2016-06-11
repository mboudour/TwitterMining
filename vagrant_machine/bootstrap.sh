#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip python-dev build-essential 
apt-get install libfreetype6-dev libpng-dev
sudo -H pip install --upgrade pip
sudo -H pip install jupyter
sudo -H pip install pandas
sudo apt-get install python-matplotlib
sudo -H pip install --upgrade matplotlib
pip install --user python-twitter
pip install --user seaborn
pip install --user lightning-python

jupyter notebook --notebook-dir=/vagrant/notebook --no-browser --ip=0.0.0.0 &