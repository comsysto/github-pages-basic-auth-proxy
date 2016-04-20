import sys, os
from bottle import route, request, response, run, hook, abort, redirect, error, install
import simplejson as json
import logging
import datetime

#
# HELPERS
#

def return_json(object, response):
    response.set_header('Content-Type', 'application/json')
    return json.dumps(object)



#
# BOTTLE APP
#
def run_proxy(env):

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
    @route('/')
    def hello():
        return 'hello there'


    #
    # RUN BY ENVIRONMENT
    #
    if env == 'dev' or env == 'local':
        run(host='localhost', port=8881, debug=True)
    else:
        run(server='cgi')

