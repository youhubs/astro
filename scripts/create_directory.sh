#!/bin/bash

# The directory where the application will be deployed
DEPLOYMENT_DIRECTORY=/var/www/html/astro-web

# Check if the directory exists
if [ ! -d "$DEPLOYMENT_DIRECTORY" ]; then
    # Create the directory if it does not exist
    mkdir -p $DEPLOYMENT_DIRECTORY
fi

# Optionally set permissions and ownership
chown ec2-user:ec2-user $DEPLOYMENT_DIRECTORY
chmod 755 $DEPLOYMENT_DIRECTORY
