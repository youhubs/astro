# Run Flask App on EC2 Instance (Linux)

## Host One Website on EC2 Instance

### Install required packages

```bash
sudo su
yum update
yum install git
yum install python3 python3-pip
```

### Clone the github repository

```bash
git clone https://github.com/youhubs/astro.git
```

### Create the virtual environment

```bash
cd  astro
python3 -m venv .venv
```

### Activate the virtual environment

```bash
source .venv/bin/activate
```

### Install required python packages

```bash
pip install -r requirements.txt
```

### Verify if it works by running

```bash
python3 app.py
```

Run Gunicorn WSGI server to serve the Flask Application
When you “run” flask, you are actually running Werkzeug’s development WSGI server, which forward requests from a web server.

Since Werkzeug is only for development, we have to use Gunicorn, which is a production-ready WSGI server, to serve our application.

### Install Gunicorn using the below command

```bash
pip install gunicorn
```

### Run Gunicorn Server

```bash
gunicorn --workers 3 --bind 0.0.0.0:8000 app:app
```

Gunicorn is running (Ctrl + C to exit gunicorn)!

Use systemd to manage Gunicorn
Systemd is a boot manager for Linux. We are using it to restart gunicorn if the EC2 restarts or reboots for some reason.

We create a **<projectname>.service** file in the /etc/systemd/system folder, and specify what would happen to gunicorn when the system reboots.

We will be adding 3 parts to systemd Unit file — Unit, Service, Install

- Unit — This section is for description about the project and some dependencies
- Service — To specify user/group we want to run this service after. Also some information about the executables and the commands.
- Install — tells systemd at which moment during boot process this service should start.
With that said, create an unit file in the /etc/systemd/system directory

```bash
vim /etc/systemd/system/astro-web.service
```

### Then add this into the file

```bash
[Unit]
Description=Gunicorn instance for Astro Web
After=network.target
[Service]
User=ec2-user
Group=nginx
WorkingDirectory=/home/ec2-user/astro
ExecStart=/home/ec2-user/astro/.venv/bin/gunicorn -b localhost:8000 app:app
Restart=always
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=astro-web
[Install]
WantedBy=multi-user.target
```

### Then enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl start astro-web
sudo systemctl enable astro-web
```

### Check if the app is running with

```bash
curl localhost:8000
```

Run Nginx Webserver to accept and route request to Gunicorn
Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.

### Install Nginx

```bash
yum install nginx
```

Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Add the following code to the config file >> **/etc/nginx/conf.d/astro-web.conf**

**Import**: this is to register the service

```json
upstream astro-web {
    server 127.0.0.1:8000;
}
```

Add a proxy_pass to astro-web at location / >> **/etc/nginx/default.d/astro.conf**

```json
location / {
    proxy_pass http://astro-web;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

### Test and Restart Nginx

```bash
sudo nginx -t
sudo systemctl restart nginx
```

## Host Two Websites on EC2 Instance

### Option 1: Different Domains (Server Blocks)

#### 1. /etc/nginx/sites-available/astro-web.conf

```json
server {
    listen 80;
    server_name astrorobotics.us;

    location / {
        proxy_pass http://astro-web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 2. /etc/nginx/sites-available/blueberry-web.conf

```json
server {
    listen 80;
    server_name blueberry.example.com; # Replace with your domain

    location / {
        proxy_pass http://blueberry-web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Create symbolic links for the files in the /etc/nginx/sites-enabled directory

For astro-web:

```bash
sudo ln -s /etc/nginx/sites-available/astro-web.conf /etc/nginx/sites-enabled/astro-web.conf
```

For blueberry-web:

```bash
sudo ln -s /etc/nginx/sites-available/blueberry-web.conf /etc/nginx/sites-enabled/blueberry-web.conf
```

### Option 2: Different Paths

#### 1. Define the Upstreams

Place these upstream definitions in **/etc/nginx/conf.d/upstreams.conf** or directly in your main Nginx configuration file (**nginx.conf**), typically under the **http** block.

```json
upstream astro-web {
    server 127.0.0.1:8000;
}

upstream blueberry-web {
    server 127.0.0.1:8001;
}
```

#### 2. Configure the Location Blocks

Then, in your server block (e.g., /etc/nginx/sites-available/default or /etc/nginx/default.d/locations.conf), set up the location directives to point to the respective upstreams based on the URL path.

```json
server {
    # ... (other server config like 'listen' and 'server_name')

    location /astro/ {
        proxy_pass http://astro-web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Optional: Strip the path prefix if your app doesn't expect it
        proxy_set_header X-Original-URI $request_uri;
        rewrite ^/astro/(.*)$ /$1 break;
    }

    location /blueberry/ {
        proxy_pass http://blueberry-web;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Optional: Strip the path prefix if your app doesn't expect it
        proxy_set_header X-Original-URI $request_uri;
        rewrite ^/blueberry/(.*)$ /$1 break;
    }
}
```
