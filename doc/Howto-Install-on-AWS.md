[![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/logo.svg)](https://github.com/comsysto/github-pages-basic-auth-proxy)

#### GitHub Pages Basic Auth Proxy by comSysto

# 3. Howto Install on AWS

We will do demo setup for the following scenario:
  
  * GitHub Page we want to secure: 
    * https://comsysto.github.io/github-pages-basic-auth-proxy/086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3/
    * This is a gh-pages branch of a public repo. In real scenario this would be a private repo and no one could guess the obfuscator.
    * Contents of gh-pages: https://github.com/comsysto/github-pages-basic-auth-proxy/tree/gh-pages  
  * Proxy-URL we want to use: 
    * https://my-secure-github-page.comsysto.com/
    * This is a `ec2.micro` Instance on AWS which is configured as described below.
    
### 3.1 Prerequisites

  * You will need nginx, python 3 and git.
    * on Ubuntu: `apt-get install git nginx python3-setuptools build-essential python3-dev`
  * optional a ssl certificate  

### 3.2 nginx setup

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

### 3.3 python proxy setup

Install proxy
```
git clone  https://github.com/comsysto/github-pages-basic-auth-proxy.git
cd github-pages-basic-auth-proxy
sudo python3 setup.py install
```

Run Proxy

  * proxy that allows only members of the organization to access page: (owner must be an GitHub Organization)

```
$> cs-gh-proxy -e wsgi -p 8881 --authType onlyGitHubOrgUsers --owner comsysto --repository github-pages-basic-auth-proxy --obfuscator 086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3
```

  * proxy that allows all GitHub Users to access page: (owner can be GitHub Organization or normal user)

```
$> cs-gh-proxy -e wsgi -p 8881 --authType allGitHubUsers --owner comsysto --repository github-pages-basic-auth-proxy --obfuscator 086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3
```

  * Howto run python server as daemon
    * first [install daemonize](http://software.clapper.org/daemonize/)
    * now create script `/opt/run-gh-proxy.sh`
    * put run command (see above) in script
    * run as daemon with `/usr/local/sbin/daemonize -p /var/run/cs-gh-proxy.pid -l /var/run/cs-gh-proxy.lock /opt/run-gh-proxy.sh`
      * Now you can write some scripts to check for pidfile or port
      * lockfile ensures that there will only be a single instance
