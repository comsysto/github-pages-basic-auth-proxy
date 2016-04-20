import sys, os
from bottle import route, request, response, run, hook, abort, redirect, error, install
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

    @route('/<url>')
    def proxy_trough(url):
        return requests.get('{0}{1}'.format(args.githubPagesUrl, url))



    #
    # RUN BY ENVIRONMENT
    #
    if args.environment == 'wsgi':
        run(host='localhost', port=8881, debug=True)
    else:
        run(server='cgi')

