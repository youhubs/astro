#!/bin/bash
# Navigate to your application directory
cd /var/www/html/astro-web

# Start your application
# If you're using Gunicorn, it might look something like this:
gunicorn -b :8000 app:app &  # Make sure to replace 'app:app' with your application details
