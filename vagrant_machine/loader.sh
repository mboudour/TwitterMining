#!/usr/bin/env bash

pip install --user --upgrade pip
pip install --user jupyter
pip install --user pandas
pip install --user numpy
pip install --user scipy
pip install --upgrade matplotlib
pip install --user python-twitter
pip install --user seaborn
pip install --user lightning-python

gpg --keyserver hkp://keys.gnupg.net --recv-keys 409B6B1796C275462A1703113804BB82D39DC0E3 7D2BAF1CF37B13E2069D6956105BD0E739499BDB
\curl -sSL https://get.rvm.io | bash -s stable --ruby
source /home/vagrant/.rvm/scripts/rvm
gem install koala
gem install pry
gem install selenium-webdriver
gem install chromedriver-helper
gem install twitter
gem install capybara

jupyter notebook --notebook-dir=/vagrant/notebook --no-browser --ip=0.0.0.0 &