from setuptools import setup

setup(name='comsysto_github_pages_basic_auth_proxy',
      version='0.0.1',
      description='Python Proxy for GitHub Pages with Basic Auth',
      url='https://github.com/comsysto/github-pages-basic-auth-proxy',
      author='comSysto GmbH',
      author_email='info@comsysto.com',
      license='MIT',
      packages=[
          'cs_proxy'
      ],
      install_requires=[
          'requests',
          'argparse',
          'validators',
          'colorama',
          'bottle',
          'simplejson',
          'python-jose'
      ],
      zip_safe=False,
      entry_points = {
          'console_scripts': ['cs-gh-proxy=cs_proxy.proxy:main'],
      })