#
# This file is part of Python-ASN1. Python-ASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# Python-ASN1 is copyright (c) 2007 by the Python-ASN1 authors. See the
# file "AUTHORS" for a complete overview.

import sys

# Support both setuptools (if installed) and distutils
try:
    from setuptools import setup, Extension
except ImportError:
    from distutils.core import setup, Extension

classifiers = \
[
    'Development Status :: 4 - Beta',
    'Environment :: Plugins',
    'Intended Audience :: Developers',
    'License :: OSI Approved :: MIT License',
    'Operating System :: Microsoft :: Windows',
    'Operating System :: POSIX',
    'Programming Language :: Python',
    'Topic :: Internet',
    'Topic :: Software Development :: Libraries :: Python Modules'
]

args = \
{
    'name': 'python-asn1',
    'version': '0.9',
    'description': 'An ASN1 encoder/decoder for Python',
    'author': 'Geert Jansen',
    'author_email': 'geert@boskant.nl',
    'url': 'http://www.boskant.nl/trac/python-asn1',
    'package_dir': {'': 'lib'},
    'py_modules': ['asn1']
}

if sys.version_info[:3] >= (2, 4, 0):
    args['classifiers'] = classifiers

setup(**args)
