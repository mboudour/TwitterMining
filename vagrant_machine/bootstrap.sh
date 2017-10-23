#!/usr/bin/env bash

apt-get update
apt-get install -y python-pip python-dev build-essential python2.7 python-dev
apt-get install libfreetype6-dev libpng-dev
apt-get install python-matplotlib
apt-get install -y build-essential autoconf libtool pkg-config python-opengl python-imaging python-pyrex python-pyside.qtopengl idle-python2.7 qt4-dev-tools qt4-designer libqtgui4 libqtcore4 libqt4-xml libqt4-test libqt4-script libqt4-network libqt4-dbus python-qt4 python-qt4-gl libgle3 python-dev libssl-dev
apt-get install libxml2-dev libxslt1-dev
apt-get install -y ipython ipython-notebook

sudo -H pip install --upgrade setuptools pip

