#!/usr/bin/env python3

##################################################################################################################################
#    ┏━╸╻  ╻    
#    ┃  ┃  ┃    
#    ┗━╸┗━╸╹    
###

# Libs ###########################################################################################################################

from backend import scan
from backend import terminal
from backend import config
from base64 import b64decode
import sys
import pprint
import socket

# Parse ##########################################################################################################################

url = ""
try:
    url = sys.argv[1]
except:
    print("Usage: %s <url>" % sys.argv[0])
    exit()

domain = url.split('://')[1].split('/')[0]
if 'https:' in url:
    port = 443
if 'http:' in url:
    port = 80
if ':' in domain:
    port = domain.split(':')[1]
    domain = domain.split(':')[0]

# Resolution & connection s#######################################################################################################

try:
    socket.gethostbyaddr(domain)
except socket.herror:
    print("Error: unable to resolve domain '%s'" % domain)
    exit()

try:
    s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    s.connect( (domain,port) )
    s.close()
    del(s)
except:
    print("Error: unable to connect to %s:%s" % (domain,port))
    exit()

# Get stats and filter results ###################################################################################################

r = scan.scan( url )

screenshot = r['screenshot_b64']
internal_links = r['internal_links']
external_links = r['external_links']
cookies = r['cookies']
headers = r['headers']
dns_answer = r['dns_answer']
subjectAltNames = r['ssl_sublectAltNames']
ssl_infos = r['ssl_infos']

del(r['dns_answer'])
del(r['screenshot_b64'])
del(r['internal_links'])
del(r['external_links'])
del(r['cookies'])
del(r['headers'])
del(r['ssl_infos'])
del(r['ssl_sublectAltNames'])

# Resolution & connection s#######################################################################################################

results = r
del(r)

terminal.title("Stats")
for k,v in results.items():
    terminal.termprint(k,v)

terminal.title("DNS")
for k,v in dns_answer.items():
    terminal.termprint(k,v)

terminal.title("SSL")
for k,v in ssl_infos.items():
    terminal.termprint(k,v)

terminal.title("SSL:subjectAltNames")
for k,v in enumerate(subjectAltNames,start=1):
    terminal.termprint(k,v[1])

terminal.title("Headers")
for k,v in headers.items():
    terminal.termprint(k,v)

terminal.title("Cookies")
for k,v in cookies.items():
    terminal.termprint(k,v)

terminal.title("Internal links")
for k,v in internal_links:
    terminal.termprint(str(k),v)

terminal.title("Extenal links")
for k,v in external_links :
    terminal.termprint(str(k),v )

## If terminal supports it, show screenshot

terminal.title("Website screenshot")
outfile = "screenshot-%s-%s.png" % (domain,config.get_date())
open(outfile,"wb").write( b64decode(screenshot) )

terminal.show_screenshot(outfile)
