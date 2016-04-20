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


