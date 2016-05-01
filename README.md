[![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/logo.svg)](https://github.com/comsysto/github-pages-basic-auth-proxy)

#### GitHub Pages Auth Basic Proxy by comSysto
A simple python based proxy to secure github pages with basic auth via a small cloud-proxy-instance.
Basic Auth checks against GitHub API. 

 
![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/basic-proxy.svg)

### Demo


| Secured Page by Auth Basic Proxy | Insecure plain GitHub Pages URL |
|--------------------------|-------------------------------|
| :closed_lock_with_key: https://my-secure-github-page.comsysto.com/ | :unlock:  [https://comsysto.github.io/github-pages-basic-auth-proxy/086e4...fe88e3/](https://comsysto.github.io/github-pages-basic-auth-proxy/086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3/) |
| You can login with your GitHub Username and password.<br>Or You can login with your GitHub Username and a [personal access token](https://help.github.com/articles/creating-an-access-token-for-command-line-use/) as password. The token does not need any scopes.  |  (normally you would not tell anyone that URL. It is just here that you see that these pages are identical) |

<br><br>

## Installation on Heroku

![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/beta-warning.svg)

<br>

### ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/step-bubble-1.svg) Create the Obfuscator directory in your gh-pages branch
<hr>

  * Create a directory with a random name (e.g. a sha256 hash) inside your gh-pages branch. <br>&nbsp;
  * ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/urls-and-obfuscator-explained.svg)

<br><br><br><br>

### ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/step-bubble-2.svg) Move Contents of gh-pages branch into obfuscator directory
<hr>

  * Move files into the obfuscator directory and create an `index.html` with some dummy content if not already present.
  * You should now be able to call the URL: 
    * `https://<owner>.github.io/<repositoryName>/<obfuscator>/index.html`

<br><br><br><br>

### ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/step-bubble-3.svg) Deploy Auth Basic Proxy to Heroku
<hr>

  * You can automatically setup the heroku instance of the proxy by clicking the deploy button.

<p align="center">
  <a href="https://heroku.com/deploy"><img src="https://www.herokucdn.com/deploy/button.svg" height="50" /></a>
</p>

  * During the install you need to specify `authType`, `Repository-Owner`, `Repository-Name` and `Obfuscator`. <br>&nbsp;
  * ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/heroku-one-click-install.gif)

<br><br><br><br>

### ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/step-bubble-4.svg) Check Installation Success Page
<hr>

  * After you clicked on the view-button you should see the *Installation Success* page. <br>&nbsp;
    * ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/heroku-deploy-success.png) <br>&nbsp;
  * When you configured the parameters correctly you should see a page like this <br>&nbsp;
    * ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/heroku-install-success.png)

<br><br><br><br>

### ![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/step-bubble-5.svg) Use the Proxy
<hr>

  * Now you can use the proxy with any url. 
  * In this example:
    * `https://nameless-cove-14005.herokuapp.com/*`

<br><br><br><br>
<br><br><br><br>

## Installation on AWS

You will need to perform step (1) and step (2) from the heroku instructions and then 
click below to see the full instructions on how to manually setup the proxy on AWS.

[![](https://comsysto.github.io/github-pages-basic-auth-proxy/public/aws-logo.png)](./doc/Howto-Install-on-AWS.md)


<br><br><br><br>
<br><br><br><br>

## X. Appendix

### X.I Roadmap

  * Provide oAuth instead of Basic Auth
  * Enable CORS
  * Enable on-the-fly GZIP compression
  * Enable caching (maybe replace internal proxy mechanism with WSGIproxy)
  * Real logging
  * Provide Ubuntu init Scripts
  * :white_check_mark: Provide Heroku easy install


### X.I License and Trademarks

  * Licensed under [MIT License](./LICENSE.md)
  * This little piece of software is brought to you by comSysto.
  * *comSysto is not a representative of GitHub. GitHub and the GitHub logos are Trademarks of GitHub inc.* 

### X.III Who needs this?

  * If you have a GitHub organization account with organization members.
  * If you have a private organization github repository.
  * If you have a `gh-pages` branch in that repository.
  * And if you want to secure the gh-pages page via basic auth, then this proxy is for you.
    * Only members of the GitHub organization OR normal GitHub users will have access
  
### X.IV What it will do


  * Proxy between GitHub Pages and User (Only GET requests)
  * Ask for Authentication (github credentials)
    * either GitHub username and password
    * Or GitHub username and access_token
  * Only proxy through if user is member of GitHub Organization or normal GitHub user (depends on how you run proxy)
  * To not have to call github api on every request we authenticate once and a [JWT Token](https://jwt.io/) is generated and stored in a cookie
    * the JWT Token is valid for 4 hours.
    * After the Token has expired or the cookie is removed you will have to perform Authentication again.
  
### X.V Is it really secure?
 
  * Basically `gh-pages` URLs are public. But if you use a private repository you can only **guess** the actual URLs. 
  * If you create a directory in your `gh-pages` branch which is called e.g. `086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3` and proxy to this dir, it will be secure as long as no one knows this **obfuscator** directory (you should keep it a secret).
  * You proxy to https (TLS) so no man in the middle attack could get a hold of the obfuscator.

### X.VI Is it fast?
 
  * The short answer is: meeeeh
  * Currently there is no real good proxy implementation in place that would cache files.
  * So for every GET request you have internal GET calls to github pages whose responses are directly returned to the user.
  * At least the Authentication is fast and optimized via JWT Auth Cookie. That reduces the auth calls on the github API.


### X.VII Styleguide

```
türkis   #1e9dcc
         #d2ebf5 
green    #99d100  
         #ebf6cc 
orange   #e67800 
blue     #1c61b3
```
