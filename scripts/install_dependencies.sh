#!/bin/bash
yum update -y
yum install -y python3
pip3 install -r /var/www/html/astro-web/requirements.txt


