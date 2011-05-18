#
# This file is part of Python-ASN1. Python-ASN1 is free software that is
# made available under the MIT license. Consult the file "LICENSE" that
# is distributed together with this file for the exact licensing terms.
#
# Python-ASN1 is copyright (c) 2007-2008 by the Python-ASN1 authors. See
# the file "AUTHORS" for a complete overview.

import sys
import os.path

import asn1
import optparse

def read_pem(input):
    """Read PEM formatted input."""
    data = []
    state = 0
    for line in input:
        if state == 0:
            if line.startswith('-----BEGIN'):
                state = 1
        elif state == 1:
            if line.startswith('-----END'):
                state = 2
            else:
                data.append(line)
        elif state == 2:
            break
    if state != 2:
        raise ValueError, 'No PEM encoded input found'
    data = ''.join(data)
    data = data.decode('base64')
    return data

def strid(id):
    """Return a string representation of a ASN.1 id."""
    if id == asn1.Boolean:
        s = 'BOOLEAN'
    elif id == asn1.Integer:
        s = 'INTEGER'
    elif id == asn1.OctetString:
        s = 'OCTET STRING'
    elif id == asn1.Null:
        s = 'NULL'
    elif id == asn1.ObjectIdentifier:
        s = 'OBJECT IDENTIFIER'
    elif id == asn1.Enumerated:
        s = 'ENUMERATED'
    elif id == asn1.Sequence:
        s = 'SEQUENCE'
    elif id == asn1.Set:
        s = 'SET'
    elif id == asn1.Null:
        s = 'NULL'
    else:
        s = '%#02x' % id
    return s
 
def strclass(id):
    """Return a string representation of an ASN.1 class."""
    if id == asn1.ClassUniversal:
        s = 'UNIVERSAL'
    elif id == asn1.ClassApplication:
        s = 'APPLICATION'
    elif id == asn1.ClassContext:
        s = 'CONTEXT'
    elif id == san1.ClassPrivate:
        s = 'PRIVATE'
    else:
        raise ValueError, 'Illegal class: %#02x' % id
    return s

def strtag(tag):
    """Return a string represenation of an ASN.1 tag."""
    return '[%s] %s' % (strid(tag[0]), strclass(tag[2]))

def prettyprint(input, output, indent=0):
    """Pretty print ASN.1 data."""
    while not input.eof():
        tag = input.peek()
        if tag[1] == asn1.TypePrimitive:
            tag, value = input.read()
            output.write(' ' * indent)
            output.write('[%s] %s (value %s)' %
                         (strclass(tag[2]), strid(tag[0]), repr(value)))
            output.write('\n')
        elif tag[1] == asn1.TypeConstructed:
            output.write(' ' * indent)
            output.write('[%s] %s:\n' % (strclass(tag[2]), strid(tag[0])))
            input.enter()
            prettyprint(input, output, indent+2)
            input.leave()


# Main script

parser = optparse.OptionParser()
parser.add_option('-p', '--pem', dest='mode', action='store_const',
                  const='pem', help='PEM encoded input')
parser.add_option('-r', '--raw', dest='mode', action='store_const',
                  const='raw', help='raw input')
parser.add_option('-o', '--output', dest='output',
                  help='output to FILE instead', metavar='FILE')
parser.set_default('mode', 'pem')
(opts, args) = parser.parse_args()

if len(args) == 1:
    input = file(sys.argv[1])
else:
    input = sys.stdin

if opts.mode == 'pem':
    input = read_pem(input)
else:
    input = input.read()

if opts.output:
    output = file(opts.output, 'w')
else:
    output = sys.stdout

data = []
for line in input:
    data.append(line)
data = ''.join(data)

dec = asn1.Decoder()
dec.start(data)

prettyprint(dec, output)
