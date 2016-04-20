# GitHhub Pages Basic Auth Proxy by comSysto

## 1. Introduction

A simple python based proxy to secure github pages via a small cloud-proxy-instance.

:bangbang: **THIS IS WORK IN PROGRESS. PRE-ALPHA** :bangbang: 
 
### 1.1 Who needs this?

  * If you have a GitHub organization account with organization members.
  * If you have a private organization github repository.
  * If you have a `gh-pages` branch in that repository.
  * And if you want to secure the gh-pages page via basic auth, then this proxy is for you.
    * Only members of the GitHub organization and users you specify manually will have access
  
### 1.2 What it will do

![](./doc/basic-proxy.png)

  * Proxy between GitHub Pages and User
  * Ask for Authentication (github credentials)
  * Only proxy through if user is member of GitHub Organization or in list of users allowed to access
  
### 1.3 How is this secure?
 
  * Basically `gh-pages` URLs are public
  * BUT if you create a directory in your `gh-pages` branch which is called `086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3` and proxy to this dir, it will be secure as long as no one knows this "obfuscator-dir"

## 2. Installation

We will do demo setup for the following scenario:
  
  * GitHub Page we want to secure: 
    * https://comsysto.github.io/github-pages-basic-auth-proxy/086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3/
    * This is a gh-pages branch of a public repo. In real scenario this would be a private repo and no one could guess the obfuscator-dirname.
    * Contents of gh-pages: https://github.com/comsysto/github-pages-basic-auth-proxy/tree/gh-pages  
  * Proxy-URL we want to use: 
    * https://my-secure-github-page.comsysto.com/
    * This is a `ec2.micro` Instance on AWS which is configured as described below.
    
### 2.1 Prerequisites

  * You will need nginx, python 3 and git.
    * on Ubuntu: `apt-get install git nginx python3-setuptools`
  * optional a ssl certificate  

### 2.2 nginx setup

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

### 2.3 python proxy setup

Install proxy
```
git clone  https://github.com/comsysto/github-pages-basic-auth-proxy.git
cd github-pages-basic-auth-proxy
sudo python3 setup.py install
```

run in background on Port 8881

```
cs-gh-proxy -e wsgi -u csgruenebe -gh https://comsysto.github.io/github-pages-basic-auth-proxy/086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3/ &
```

