from .proxy import run_proxy

import argparse
import sys
import colorama
import requests

def main():
    #
    # CLI PARAMS
    #
    parser = argparse.ArgumentParser(description='comSysto GitHub Pages Auth Basic Proxy')

    parser.add_argument("-e", "--environment", help='Which environment.', choices=['cgi', 'wsgi'])
    parser.add_argument("-gh", "--githubPagesUrl", help='baseUrl to gh-pages page e.g. https://foo.github.io/repo/2323/')
    parser.add_argument("-u", "--allowedUsers", help='allowed usernames.')

    args = parser.parse_args()
    if not args.environment:
        print ('USAGE')
        print ('    proxy:')
        print ('      $> cs-gh-proxy -e wsgi -u csgruenebe -gh https://comsysto.github.io/github-pages-basic-auth-proxy/086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3/ ')
        print ('')

        sys.exit(1)

    run_proxy(args.environment)
