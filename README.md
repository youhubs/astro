# Run Flask App on EC2 Instance (Linux)

## 1. Host One Website on EC2 Instance

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

### Prepare for Running Flask App

#### Create the virtual environment

```bash
cd  astro
python3 -m venv .venv
```

#### Activate the virtual environment

```bash
source .venv/bin/activate
```

#### Install required python packages

```bash
pip install -r requirements.txt
```

#### Verify if it works by running

```bash
python3 app.py
```

Run Gunicorn WSGI server to serve the Flask Application
When you “run” flask, you are actually running Werkzeug’s development WSGI server, which forward requests from a web server.

Since Werkzeug is only for development, we have to use Gunicorn, which is a production-ready WSGI server, to serve our application.

### Install & Setup Gunicorn Server

#### Install Gunicorn

```bash
pip install gunicorn
```

#### Run Gunicorn Server

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
vim /etc/systemd/system/web-astro.service
```

#### Then add this into the file

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
StandardOutput=journal
StandardError=journal
SyslogIdentifier=web-astro
[Install]
WantedBy=multi-user.target
```

#### Then enable the service

```bash
sudo systemctl daemon-reload
sudo systemctl start web-astro
sudo systemctl enable web-astro
```

#### Check if the app is running with

```bash
curl localhost:8000
```

Run Nginx Webserver to accept and route request to Gunicorn
Finally, we set up Nginx as a reverse-proxy to accept the requests from the user and route it to gunicorn.

### Install Nginx and Configuration

```bash
yum install nginx
```

Start the Nginx service and go to the Public IP address of your EC2 on the browser to see the default nginx landing page

```bash
sudo systemctl start nginx
sudo systemctl enable nginx
```

Add the following code to the config file >> **/etc/nginx/conf.d/web-astro.conf**

**Import**: this is to register the service

```json
upstream web-astro {
    server 127.0.0.1:8000;
}
```

Add a proxy_pass to web-astro at location / >> **/etc/nginx/default.d/astro.conf**

```json
location / {
    proxy_pass http://web-astro;
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

## 2. Host Two Websites on EC2 Instance

### First Define the Upstreams

Place these upstream definitions in **/etc/nginx/conf.d/upstreams.conf** or directly in your main Nginx configuration file (**nginx.conf**), typically under the **http** block.

```json
upstream web-astro {
    server 127.0.0.1:8000;
}

upstream web-blueberry {
    server 127.0.0.1:8001;
}
```

### Option 1: Different Domains (Server Blocks)

#### 1. /etc/nginx/sites-available/web-astro.conf

```json
server {
    listen 80;
    server_name astrorobotics.us;

    location / {
        proxy_pass http://web-astro;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 2. /etc/nginx/sites-available/web-blueberry.conf

```json
server {
    listen 80;
    server_name blueberry.example.com; # Replace with your domain

    location / {
        proxy_pass http://web-blueberry;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

#### 3. Create symbolic links for the files in the /etc/nginx/sites-enabled directory

For web-astro:

```bash
sudo ln -s /etc/nginx/sites-available/web-astro.conf /etc/nginx/sites-enabled/web-astro.conf
```

For web-blueberry:

```bash
sudo ln -s /etc/nginx/sites-available/web-blueberry.conf /etc/nginx/sites-enabled/web-blueberry.conf
```

### Option 2: Different Paths

#### 1. Configure the Location Blocks

In your server block (e.g., /etc/nginx/sites-available/default or /etc/nginx/default.d/locations.conf), set up the location directives to point to the respective upstreams based on the URL path.

```json
server {
    # ... (other server config like 'listen' and 'server_name')

    location /astro/ {
        proxy_pass http://web-astro;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        # Optional: Strip the path prefix if your app doesn't expect it
        proxy_set_header X-Original-URI $request_uri;
        rewrite ^/astro/(.*)$ /$1 break;
    }

    location /blueberry/ {
        proxy_pass http://web-blueberry;
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

## Add One More Server to EC2 Instance

- Add a new Gunicorn Service

- Add the new service to /etc/nginx/conf.d/upstreams.conf

- Add a new Nginx server to /etc/nginx/sites-available/

## Common Used Commands

### Gunicorn Services Handling

Make sure your Gunicorn instances for both web-astro and web-blueberry are running and listening on the correct ports (8000 and 8001).

```bash
sudo systemctl status web-astro.service
sudo systemctl status web-blueberry.service
# Other commands
sudo systemctl daemon-reload 
sudo systemctl start service_name.service 
sudo systemctl restart service-name.service 
sudo systemctl enable service-name.service 
sudo systemctl status service-name.service 
sudo systemctl reload service_name.service 
sudo systemctl disable service_name.service 
sudo systemctl stop service-name 
```

### Port Handling

```bash
sudo netstat -tulnp | grep ':8000' 
sudo ss -tulnp | grep ':8000' 
sudo kill PID 
sudo kill PID1 PID2 ... 
sudo systemctl stop service-name  # kill all the services
```

### Gunicorn Service Logging

```bash
sudo tail -f /var/log/nginx/access.log 
sudo tail -f /var/log/nginx/error.log 

sudo journalctl -u service-name.service 
sudo journalctl -u service-name.service | grep 'some search term' 
```

### Nginx Server Handling

```bash
sudo nginx -t 
sudo systemctl reload nginx 
sudo systemctl restart nginx 
sudo systemctl status nginx 
```

### Curl Handling

```bash
curl localhost:5000/webhook 
curl -X POST localhost:5000/webhook 
curl http://astrorobotics.us 
curl -I http://astrorobotics.us 
curl -v http://astrorobotics.us 
curl -X POST -H "Content-Type: application/json" -d '{"test": "data"}' localhost:8003/webhook 
curl -X POST http://127.0.0.1:8005/webhook -H "Content-Type: application/json" -d '{"key": "value"}' 
```

### Test Network Connectivity

```bash
ping 3.145.36.230 
traceroute 3.145.36.230 
```
