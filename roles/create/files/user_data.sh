#!/bin/bash

# Update the package list
sudo apt update

# Upgrade all installed packages
sudo DEBIAN_FRONTEND=noninteractive apt-get -yq upgrade
sudo apt upgrade -y

# Install Ansible
sudo apt install software-properties-common -y
sudo add-apt-repository --yes --update ppa:ansible/ansible
sudo apt update
sudo apt install ansible -y

echo "Ansible installation and initial setup complete" > /tmp/setup.log