#!/bin/bash

# Update the package list
sudo yum update -y

# Install Docker
sudo yum install docker -y

sudo yum install git -y
# Start and enable Docker
sudo systemctl start docker
sudo systemctl enable docker

# Add the current user (ec2-user) to the docker group
sudo usermod -aG docker ec2-user

# Download Docker Compose and set the permissions
sudo curl -L "https://github.com/docker/compose/releases/download/v2.29.0/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Install Python and pip
sudo yum install python3 -y
sudo yum install python3-pip -y

# Source the .bashrc file to apply the changes
source ~/.bashrc

cd home/ec2-user

git clone https://github.com/Dakini/MLops_project.git
cd prima-diabetes-mlops
git checkout remote
