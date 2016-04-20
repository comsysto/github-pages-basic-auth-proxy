import sys, os
from bottle import route, request, response, run, hook, abort, redirect, error, install, auth_basic
import simplejson as json
import logging
import datetime
import requests


#
# HELPERS
#
def return_json(object, response):
    response.set_header('Content-Type', 'application/json')
    return json.dumps(object)

def check_pass(username, password):
    if username == 'bob' and password == '5678':
        return True
    return False

def normalize_proxy_url(url):
    print ('URL:')
    print (url)
    if url.endswith('/') or url == '':
        return '{0}index.html'.format(url)
    return url

def proxy_trough_helper(url):
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


    @route('/<url:re:.+>')
    @auth_basic(check_pass)
    def proxy_trough(url):
        return proxy_trough_helper('{0}{1}'.format(args.githubPagesUrl, normalize_proxy_url(url)))

    @route('/')
    @auth_basic(check_pass)
    def proxy_trough_root_page():
        return proxy_trough_helper('{0}{1}'.format(args.githubPagesUrl, '/index.html'))


    #
    # RUN BY ENVIRONMENT
    #
    if args.environment == 'wsgi':
        run(host='localhost', port=8881, debug=True)
    else:
        run(server='cgi')

