# Web-Query
<i>web-monitor-flask</i>

## Dependencies

### Debian install

```sh
apt-get -y install \
	python3-venv \
	python3-pip \
	libwoff1 \
	libevent-2.1-7 \
	libgstreamer-plugins-base1.0-0 \
	gstreamer1.0-plugins-base \
	libharfbuzz-icu0 \
	libenchant-2-2 \
	libsecret-1-0 \
	libhyphen0 \
	libmanette-0.2-0 \
	libgles2 \
	libgstreamer-gl1.0-0 \
	libgstreamer-plugins-bad1.0-0 \
	libflite1 \
	libx264-* \
	libcups2 \
	libnspr4 \
	libatk1.0-0 \
	libatk-bridge2.0-0 \
	libpango-1.0-0 \
	libxrandr2 \
	libxdamage1 \
	libxcomposite1 \
	libatk-bridge2.0-0 \
	libatspi2.0-0 \
	libnss3 \
	libxcursor1 \
	libgtk-3-0 \
	librust-gdk-sys-dev \
	libvpx7
	git \
	curl
```

### Set virtuel env for python

```sh
cd web-monitor-flask/
python3 -m venv .
pip install -r requirements.txt
```

### Install playwright (for web sites screenshot)

```sh
# Download of headless web browsers
playwright install
```

## Local server execution

Start the server by running `python server.py`
Then go to `http://127.0.0.1:5000`

## Automation of request

```sh
# Through Flask
curl 'https://127.0.0.1:5000/report' --compressed -X POST --data 'url=https://app.site.com/' -o report.html

# report.py for a HTML report ordered by date
python3 report.py 'https://app.site.com/'

# cli.py for text report
python3 cli.py 'https://app.site.com/'
```

## Quick deploy on Apache

To quickly deploy it on a server, in your Apache config, set a reverse proxy : 

In your `/etc/apache2/sites-enabled/099-app.site.com.conf` : 

```
<VirtualHost *:80>
  ServerName app.site.com
  ServerAdmin webmaster@site.com
  ErrorLog /dev/null
  CustomLog /dev/null combined
  RewriteEngine on
  RewriteCond %{SERVER_NAME} =app.site.com
  RewriteRule ^ https://%{SERVER_NAME}%{REQUEST_URI} [END,NE,R=permanent]
</VirtualHost>
```

In your `/etc/apache2/sites-enabled/099-app.site.com-le-ssl.conf` : 

```
<IfModule mod_ssl.c>
  <VirtualHost *:443>
    ServerName app.site.com
    ServerAdmin webmaster@site.com
    DocumentRoot /var/www/sites/app.site.com
    # ErrorLog ${APACHE_LOG_DIR}/error-app.site.com.log
    ErrorLog /dev/null
    CustomLog /dev/null combined
    # CustomLog ${APACHE_LOG_DIR}/access-app.site.com.log combined
    ProxyPass / http://127.0.0.1:5000/ nocanon
    ProxyPassReverse / http://127.0.0.1/
    SSLCertificateFile /etc/letsencrypt/live/app.site.com/fullchain.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/app.site.com/privkey.pem
    Include /etc/letsencrypt/options-ssl-apache.conf
  </VirtualHost>
</IfModule>
```

