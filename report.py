#!/usr/bin/env python3

##################################################################################################################################
#    ┏━┓┏━╸┏━┓┏━┓┏━┓╺┳╸   ╻ ╻╺┳╸┏┳┓╻
#    ┣┳┛┣╸ ┣━┛┃ ┃┣┳┛ ┃    ┣━┫ ┃ ┃┃┃┃
#    ╹┗╸┗━╸╹  ┗━┛╹┗╸ ╹    ╹ ╹ ╹ ╹ ╹┗━╸
###

# Libs ###########################################################################################################################

from flask import Flask, render_template, request, redirect, url_for, session
from backend import scan
from backend import html
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
    socket.gethostbyname(domain)
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

current_date = config.get_date()
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

# Note: hd = Html Data
#       bt = BoTtom html 

hd = open("templates/static/top.html","r").read()
bt = open("templates/static/bottom.html","r").read()

hd = hd.replace( '__DOMAIN__'                   , domain )
hd = hd.replace( '__DATETIME__'                 , results['datetime'] )
hd = hd.replace( '__URL__'                      , results['url']    )
hd = hd.replace( '__TITLE__'                    , results['title']  )
hd = hd.replace( '__HACKED_KEYWORDS__'          , results['hacked_keywords']  )
hd = hd.replace( '__ELAPSED_TIME__'             , str(results['elapsed_u'])  )
hd = hd.replace( '__DIGEST__'                   , results['digest']  )
hd = hd.replace( '__CONTENT_HASH__'             , results['content_hash']  )
hd = hd.replace( '__HEADERS_HASH__'             , results['headers_hash']  )
hd = hd.replace( '__HTML_HEADER_SECTION_HASH__' , results['html_header_section_hash']  )
hd = hd.replace( '__X_GENERATOR__'              , results['x_generator']  )
hd = hd.replace( '__SERVER__'                   , results['server']  )
hd = hd.replace( '__X_POWERED_BY__'             , results['x_powered_by']  )
hd = hd.replace( '__NB_CSS__'                   , str(results['nb_css'])  )
hd = hd.replace( '__NB_JS__'                    , str(results['nb_js'])  )
hd = hd.replace( '__NB_IMG__'                   , str(results['nb_img'])  )

hd = hd.replace( '__SCREENSHOT_B64__'   , screenshot )

hd += html.write_table (
    title="DNS answers",
    table=dns_answer,
    html_class={
        "table": "border",
        "th": "key",
        "td": "val"
    }
)

hd += html.h2("SSL Informations")

hd += html.write_table (
    title="Certificat",
    table=ssl_infos,
    html_class={
        "table": "border",
        "th": "key",
        "td": "val"
    }
)

hd += html.write_div (
    title="SSL:Altnames",
    values=enumerate(subjectAltNames, start=1),
    html_class={
        "div": "overflow-container",
        "table": "border",
        "th": "index",
        "td": "val"
    }
)

hd += html.h2("Responses")

hd += html.write_table (
    title="Headers",
    table=headers,
    html_class={
        "table": "border",
        "th": "key",
        "td": "val"
    }
)

hd += html.write_table (
    title="Cookies",
    table=cookies,
    html_class={
        "table": "border",
        "th": "key",
        "td": "val"
    }
)

hd += html.h2("Links")

hd += html.write_div (
    title="External",
    values=enumerate(external_links, start=1),
    html_class={
        "div": "overflow-container",
        "table": "border",
        "th": "index",
        "td": "val"
    }
)

hd += html.write_div (
    title="Internal",
    values=enumerate(internal_links, start=1),
    html_class={
        "div": "overflow-container",
        "table": "border",
        "th": "index",
        "td": "val"
    }
)

bt = bt.replace( '__URL__'              , results['url'])
bt = bt.replace( '__RESPONSE_TIME1__'   , str(results['response_time1'])    )
bt = bt.replace( '__RESPONSE_TIME2__'   , str(results['response_time2'])    )
bt = bt.replace( '__RESPONSE_TIME3__'   , str(results['response_time3'])    )
bt = bt.replace( '__RESPONSE_TIME4__'   , str(results['response_time4'])    )
bt = bt.replace( '__RESPONSE_TIME5__'   , str(results['response_time5'])    )

hd += bt

del(bt)
del(results) # free memory

# chart_js = open("static")
outfile = html.save_report(hd,domain,current_date)

print(outfile)

