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
    parser.add_argument("-gho", "--owner", help='the owner of the repository. Either organizationname or username.')
    parser.add_argument("-ghr", "--repository", help='the repository name.')
    parser.add_argument("-obf", "--obfuscator", help='the subfolder-name in gh-pages branch used as obfuscator')
    parser.add_argument("-p", "--port", help='the port to run proxy e.g. 8881')
    parser.add_argument("-a", "--authType", help='how should users auth.', choices=['allGitHubUsers', 'onlyGitHubOrgUsers'] )


    args = parser.parse_args()
    if not args.environment:
        print ('USAGE')
        print ('    proxy that allows only members of the organization to access page: (owner must be an GitHub Organization)')
        print ('      $> cs-gh-proxy -e wsgi -p 8881 --authType onlyGitHubOrgUsers --owner comsysto --repository github-pages-basic-auth-proxy --obfuscator 086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3')
        print ('')
        print ('    proxy that allows all GitHub Users to access page: (owner can be GitHub Organization or normal user)')
        print ('      $> cs-gh-proxy -e wsgi -p 8881 --authType allGitHubUsers --owner comsysto --repository github-pages-basic-auth-proxy --obfuscator 086e41eb6ff7a50ad33ad742dbaa2e70b75740c4950fd5bbbdc71981e6fe88e3')
        print ('')

        sys.exit(1)

    run_proxy(args)
