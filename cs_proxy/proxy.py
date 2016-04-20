import sys, os
from bottle import route, request, response, run, hook, abort, redirect, error, install, auth_basic
import simplejson as json
import random
import logging
import datetime
import requests
from requests.auth import HTTPBasicAuth
from jose import jwt
from jose.exceptions import JWSError
import datetime

#
# global vars
#
owner = 0
auth_type = 0
jwt_secret = "%032x" % random.getrandbits(128)

#
# HELPERS
#
def return_json(object, response):
    response.set_header('Content-Type', 'application/json')
    return json.dumps(object)

def create_jwt_token():
    return jwt.encode({'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=4)}, jwt_secret, algorithm='HS256')


def valid_jwt_token(token):
    try:
        res = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        print (res)
        return True
    except JWSError:
        return False

def check_pass(username, password):
    #
    # First check if already valid JWT Token in Cookie
    #
    auth_cookie = request.get_cookie("cs-proxy-auth")
    if auth_cookie and valid_jwt_token(auth_cookie):
        print ('PROXY-AUTH: found valid JWT Token in cookie')
        return True

    #
    # GitHub Basic Auth - also working with username + personal_access_token
    #
    print ('PROXY-AUTH: doing github basic auth - authType: {0}, owner: {1}'.format(auth_type, owner))
    basic_auth = HTTPBasicAuth(username, password)
    auth_response = requests.get('https://api.github.com/user', auth=basic_auth)
    if auth_response.status_code == 200:
        if auth_type == 'onlyGitHubOrgUsers':
            print ('PROXY-AUTH: doing org membership request')
            org_membership_response = requests.get('https://api.github.com/user/orgs', auth=basic_auth)
            if org_membership_response.status_code == 200:
                for org in org_membership_response.json():
                    if org['login'] == owner:
                        response.set_cookie("cs-proxy-auth", create_jwt_token())
                        return True
                return False
        else:
            response.set_cookie("cs-proxy-auth", create_jwt_token())
            return True
    return False


def normalize_proxy_url(url):
    print ('URL:')
    print (url)
    if url.endswith('/') or url == '':
        return '{0}index.html'.format(url)
    return url

def proxy_trough_helper(url):
    print ('PROXY-GET: {0}'.format(url))
    proxy_response = requests.get(url)
    response.set_header('Last-Modified', proxy_response.headers['Last-Modified'])
    response.set_header('Content-Type',  proxy_response.headers['Content-Type'])
    response.set_header('Expires',       proxy_response.headers['Expires'])
    return proxy_response


#
# BOTTLE APP
#
def run_proxy(args):

    #
    # ERROR HANDLERS
    #
    @error(401)
    def error404(error):
        return json.dumps({ 'error': error.body })

    @error(500)
    def error500(error):
        return json.dumps({ 'error': error.body })

    #
    # SPECIAL ENDPOINTS
    #
    @route('/health')
    def hello():
        return 'ok'

    #
    # make args available in auth callback
    #
    global owner, auth_type
    owner = args.owner
    auth_type = args.authType

    @route('/<url:re:.+>')
    @auth_basic(check_pass)
    def proxy_trough(url):
        return proxy_trough_helper('https://{0}.github.io/{1}/{2}/{3}'.format(args.owner, args.repository, args.obfuscator, normalize_proxy_url(url)))

    @route('/')
    @auth_basic(check_pass)
    def proxy_trough_root_page():
        return proxy_trough_helper('https://{0}.github.io/{1}/{2}/{3}'.format(args.owner, args.repository, args.obfuscator, '/index.html'))

    #
    # RUN BY ENVIRONMENT
    #
    if args.environment == 'wsgi':
        run(host='localhost', port=args.port, debug=True)
    else:
        run(server='cgi')

