# Web-Monitor-Flask

__Made assisted with chatGPT 4__

## Dependencies

```sh
pip install -r requirements.txt

apt-get install libwoff1 libevent-2.1-7 libgstreamer-plugins-base1.0-0 gstreamer1.0-plugins-base \
   libharfbuzz-icu0 libenchant-2-2 libsecret-1-0 libhyphen0 libmanette-0.2-0 \
   libgles2 libgstreamer-gl1.0-0 libgstreamer-plugins-bad1.0-0

# Download of headless web browsers
playwright install
```

## Local execution

Start the server by running `python server.py`
Then go to `http://127.0.0.1:5000`

## Automation of request

```sh
curl 'https://127.0.0.1:5000/report' --compressed -X POST --data 'url=https://app.site.com/' -o report.html
```

## Quick and dirty deploy on Apache

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


