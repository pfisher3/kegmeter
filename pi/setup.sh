#!/bin/bash

# Starting from a minimal install of Raspbian
# from https://dl.dropbox.com/u/45842273/2012-07-15-wheezy-raspian-minimal.img.7z

# Update packages and fix locale
export DEBIAN_FRONTEND=noninteractive
sudo apt-get update
sudo apt-get -y install locales
sudo apt-get -y upgrade -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold"

# Install required packages
sudo apt-get -y -o Dpkg::Options::="--force-confdef" -o Dpkg::Options::="--force-confold" install \
  git lxde python python-dev python-pip libsqlite3-dev memcached

# Create kegmeter user and download application
sudo useradd -m -s /bin/bash kegmeter

sudo mkdir -p /data
sudo chown kegmeter /data
( cd /data && sudo -u kegmeter git clone https://github.com/Dennovin/kegmeter.git )

# Set up autologin/autostart
cat | sudo tee /etc/lightdm/lightdm.conf <<EOF
[LightDM]

[SeatDefaults]
autologin-user=kegmeter
autologin-user-timeout=0
xserver-allow-tcp=false
session-wrapper=/etc/X11/Xsession

[XDMCPServer]

[VNCServer]

EOF

sudo -u kegmeter mkdir -p /home/kegmeter/.config/autostart
cat | sudo -u kegmeter tee /home/kegmeter/.config/autostart/kegmeter <<EOF
[Desktop Entry]
Type=Application
Exec=/data/kegmeter/app/app.py
EOF

# Download PT Sans font
wget https://www.google.com/fonts/download?kit=-tlFHQ-l0RbFTifjjgYkyKCWcynf_cDxXwCLxiixG1c -O /tmp/fonts.zip
sudo -u kegmeter mkdir -p /home/kegmeter/.fonts
sudo -u kegmeter unzip /tmp/fonts.zip -d /home/kegmeter/.fonts

# Install Python requirements
sudo pip install /data/kegmeter/app

# Initialize the database
sudo -u kegmeter /data/kegmeter/app/app.py --init-db

# Reboot... and hopefully everything works
sudo reboot