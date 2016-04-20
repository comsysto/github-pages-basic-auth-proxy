# GitHhub Pages Basic Auth Proxy 
## by comSysto

A simple python based proxy to secure github pages via a small cloud-proxy-instance.

:bangbang: THIS IS WORK IN PROGRESS. PRE-ALPHA :bangbang: 
 
### Who needs this?

If you have a private github repository.
If you have a `gh-pages` branch in that repository.
And if you want to secure the gh-pages page via basic auth, then this proxy is for you

### What it will do

![](./doc/basic-proxy.png)

  * Proxy between GitHub Pages and User
  * Ask for Authentication
  * Only proxy through if user is member of GitHub Organization or in list of users allowed to access
  
### How is this secure?
 
  * Basically `gh-pages` URLs are public
  * BUT if you create a directory in your `gh-pages` branch which is called `ibjsda67d79gds8a9sd88` and proxy to this dir, it will be secure as long as no one knows this "obfuscator-dir"

# Installation

We will do demo setup for the following scenario:
  
  * GitHub Page we want to secure: 
  ** https://comsysto.github.io/github-pages-basic-auth-proxy/086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3/
  ** (this is a gh-pages branch of a public repo. In real scenario this would be a private repo)
  ** Contents of gh-pages: https://github.com/...  
  * Proxy-URL we want to use: 
  ** https://my-secure-github-page.comsysto.com/
  ** This is a `ec2.micro` Instance on AWS.
    
## Prerequisites

  * You will need nginx and python.

## nginx setup

We need some kind of vhost with SSL that proxies everything through to our python proxy.

```
server {
    listen 443;
    server_name my-secure-github-page.comsysto.com;

    ssl on;
    ssl_certificate /etc/ssl/comsysto.crt;
    ssl_certificate_key /etc/ssl/comsysto.key;
    ssl_session_timeout 5m;
    ssl_protocols SSLv3 TLSv1 TLSv1.1 TLSv1.2;
    ssl_ciphers "HIGH:!aNULL:!MD5 or HIGH:!aNULL:!MD5:!3DES";
    ssl_prefer_server_ciphers on;
    
    location / {
        proxy_pass http://127.0.0.1:8881/;
    }
}
```

## python proxy setup

The python proxy runs as WSGI standalone process on port 8881.

```
python run_proxy_prod.py &
```

