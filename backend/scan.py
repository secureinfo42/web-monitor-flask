##################################################################################################################################
#    ┏━┓┏━╸┏━┓┏┓╻    
#    ┗━┓┃  ┣━┫┃┗┫    
#    ┗━┛┗━╸╹ ╹╹ ╹    
###

# Libs ###########################################################################################################################

from backend import config           # backend/config.py
from backend import ssl              # -
from backend import pwnd             # check for pwning
from backend import hasher           # make hash
from backend import dns              # dns resolver
from backend import screenshoter     # playwright wrapper

from bs4 import BeautifulSoup as bs  # xml/html parser
from datetime import datetime        # -
import requests                      # web requests (get)
import warnings                      # ignore warnings (ssl)
import re                            # regex
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")

# Funcz ##########################################################################################################################

## Use folding to increase readibility

def get_date():
  """
  Return current date

  Params: none
  Returns: string
  """

  current_datetime = datetime.now()
  return( current_datetime.strftime('%Y-%m-%d %H:%M:%S') )

def wgetping(s,url,count=5):
  """
  Do N http(s) request

  Params: session: requests.session, url: string, count: int
  Returns: tuples
  """

  results = []
  for i in range(count):
    r = s.get(url,verify=False,headers=config.Headers)
    results.append( r.elapsed.microseconds )
    del(r)
  return(results) # [0],t[1],t[2],t[3],t[4])

def get_external_links(buff,domain):
  """
  Get external links
  
  Params: session, url, count
  Returns: tuples
  """

  external_links = []
  for l in re.findall(r'(https?://.+?)[\b\'"]',buff):
    if domain not in l and '://' in l:
      external_links.append(l)
  return( sorted([ u for u in set(external_links) ]) )

def is_internal_link(l,k,d):
  """
  Get internal links, check link:href, script:src, a:href, img:src
  
  Params: link (l), key (k), domain (d)
  Returns: boolean
  """

  try:
    u = str(l[k])
    if d in str(u) or '://' not in str(u):
      return(True)
  except:
    pass
  return(False)

def get_internal_links(html,domain):
  """
  Get internal links
  
  Params: html body, domain
  Returns: tuples
  """

  internal_links = []
  for l in html('link'):
    if is_internal_link(l,'href',domain):
      internal_links.append( l['href'] )
  for l in html('script'):
    if is_internal_link(l,'src',domain):
      internal_links.append( l['src'] )
  for l in html('a'):
    if is_internal_link(l,'href',domain):
      internal_links.append( l['href'] )
  for l in html('img'):
    if is_internal_link(l,'src',domain):
      internal_links.append( l['src'] )
  return( sorted([ u for u in set(internal_links) ]) )

def scan(url):
  """
  Get stats, ssl infos, dns infos and html stats of url
  
  Params: url
  Returns: dict
  """

  ## Init vars -------------------------------------------------------------------------------------------------------------------

  d = {}
  s = requests.session()

  ## DNS resolution test ---------------------------------------------------------------------------------------------------------

  domain = url.split('://')[1].split('/')[0]
  if ':' in domain:
      domain = domain.split(':')[0]
  dns_answer = dns.dns_resolve(domain)

  ## Connection test -------------------------------------------------------------------------------------------------------------

  try:
    r = s.get(url,verify=False,headers=config.Headers)
  except KeyboardInterrupt:
    return("error:operation_aborted")
    exit()
  except:
    return("error:no_connection")
    exit()

  ## wgetping --------------------------------------------------------------------------------------------------------------------

  response_times = wgetping(s,url)

  ## html parsing ----------------------------------------------------------------------------------------------------------------

  html = bs(r.text)
  title = ""
  try:
    title = html('title')[0].text
  except:
    try:
      title = r.text.lower().split('<title>')[1].split('</title>')[0]
    except:
      title = "Unknown"

  ## html parsing (tag counter) --------------------------------------------------------------------------------------------------

  nb_css = len(re.findall(r'<\s*link[a-zA-Z0-9_"\'\-/\s\.=#\&,\?\(\)\[\]]+.css.*?>',r.text.lower()))
  nb_js  = len(re.findall(r'<\s*script[a-zA-Z0-9_"\'\-/\s\.=#\&,\?\(\)\[\]]+.js.*?>',r.text.lower()))
  nb_img = len(re.findall(r'<\s*img\b',r.text.lower()))
  headers = r.headers

  ## cookie ----------------------------------------------------------------------------------------------------------------------

  cookies = r.cookies
  if len(str(cookies)) < 1:
    cookies = "None"

  ## check for pwn keywords ------------------------------------------------------------------------------------------------------

  hacked_keywords = pwnd.check(r.text)

  ## hash ------------------------------------------------------------------------------------------------------------------------

  content_hash = hasher.gethash(r.text)
  raw_headers = ""
  for x in r.headers:
    if "date" in x.lower() or "modified" in x.lower()  or "expire" in x.lower()  or "cookie" in x.lower() :
      continue
    raw_headers += x + ":" + r.headers[x]

  headers_hash = hasher.gethash(str(raw_headers))

  try:    html_header_section_hash = hasher.gethash(r.text.split('<html')[1].split('<body')[0])
  except: html_header_section_hash = hasher.gethash(r.text[:1024])

  ## get links -------------------------------------------------------------------------------------------------------------------

  internal_links = get_internal_links(html,domain)
  external_links = get_external_links(r.text,domain)

  ## try to get server/app version through answers' headers ----------------------------------------------------------------------

  x_powered_by, x_generator, server = 'Unknown','Unknown','Unknown'

  if 'X-Generator' in r.headers:  x_generator  = r.headers['X-Generator']
  if 'X-Powered-By' in r.headers: x_powered_by = r.headers['X-Powered-By']
  if 'Server' in r.headers:       server       = r.headers['Server']

  ## ssl information -------------------------------------------------------------------------------------------------------------
  
  ssl_infos       = ssl.get_ssl_infos(domain)
  sublectAltNames = ssl_infos['subjectAltNames']
  del(ssl_infos['subjectAltNames'])
  screenshot_b64  = screenshoter.take_screenshot(url)
  elapsed_u       = r.elapsed.microseconds

  ret = {
    'url': url,
    'title': title,
    'content_hash': content_hash,
    'headers_hash': headers_hash,
    'html_header_section_hash': html_header_section_hash,
    'x_generator': x_generator,
    'x_powered_by': x_powered_by,
    'server': server,
    'ssl_infos': ssl_infos,
    'ssl_sublectAltNames': enumerate(sublectAltNames,start=1),
    'ssl_sublectAltNames_nb': len(sublectAltNames),
    'cookies': cookies,
    'headers': headers,
    'elapsed_u': elapsed_u,
    'hacked_keywords': hacked_keywords,
    'datetime': get_date(),
    'screenshot_b64': screenshot_b64,
    'domain': domain,
    'response_time1': response_times[0],
    'response_time2': response_times[1],
    'response_time3': response_times[2],
    'response_time4': response_times[3],
    'response_time5': response_times[4],
    'digest': config.DIGEST,
    'nb_css': nb_css,
    'nb_js': nb_js,
    'nb_img': nb_img,
    'external_links': enumerate(external_links,start=1),
    'external_links_nb': len(external_links),
    'internal_links': enumerate(internal_links,start=1),
    'internal_links_nb': len(internal_links),
    'dns_answer': dns_answer,
  }

  #TODO: see how to parse array for js
  # for t in response_times:
  #   ret.update( {} )

  return(ret)

# Main ###########################################################################################################################

if __name__ == '__main__':
  from sys import argv
  try:
    url = argv[1]
  except:
    print("Usage: %s <url>" % argv[0])
    exit()
  ret = scan(url)
  print(ret)
