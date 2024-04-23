#analyze_url

import requests
from backend import config
from backend import cert_ssl
from backend import web_pwnd
from backend import make_hash
from bs4 import BeautifulSoup as bs
from datetime import datetime
from backend import screenshoter

import warnings
import logging
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def get_date():
  current_datetime = datetime.now()
  return( current_datetime.strftime('%Y-%m-%d %H:%M') )

def web_ping(s,url,count=5):

  t = []
  for i in range(count):
    r = s.get(url,verify=False,headers=config.Headers)
    t.append( r.elapsed.microseconds )
    del(r)

  return(t[0],t[1],t[2],t[3],t[4])

def scan(url):

  d = {}
  s = requests.session()

  r = s.get(url,verify=False,headers=config.Headers)

  t1,t2,t3,t4,t5 = web_ping(s,url)

  html = bs(r.text)
  title = ""
  try:
    title = html('title')[0].text
  except:
    try:
      title = r.text.lower().split('<title>')[1].split('</title>')[0]
    except:
      title = "Unknown"
  cookies = r.cookies
  if len(str(cookies)) < 1:
    cookies = "Aucun"

  headers = r.headers
  hacked_keywords = web_pwnd.check(r.text)
  content_hash = make_hash.make_hash(r.text)
  raw_headers = ""
  for x in r.headers:
    if x.lower() == "date":
      continue
    raw_headers += x + ":" + r.headers[x]
  headers_hash = make_hash.make_hash(str(raw_headers))
  try:
    header_section_hash = make_hash.make_hash(r.text.split('<html')[1].split('<body')[0])
  except:
    header_section_hash = make_hash.make_hash(r.text[:1024])

  x_generator = 'Unknown'
  try: x_generator = r.headers['X-Generator']
  except: pass

  x_powered_by = 'Unknown'
  try: x_powered_by = r.headers['X-Powered-By']
  except: pass

  server = 'Unknown'
  try: server = r.headers['Server']
  except: pass

  domain = url.split('/')[2]
  ssl_expiry = cert_ssl.get_ssl_expiry_date(domain)

  screenshot_b64 = screenshoter.take_screenshot(url)

  elapsed_u = r.elapsed.microseconds

  return({
    'url': url,
    'title': title,
    'content_hash': content_hash,
    'headers_hash': headers_hash,
    'header_section_hash': header_section_hash,
    'x_generator': x_generator,
    'x_powered_by': x_powered_by,
    'server': server,
    'ssl_expiry': ssl_expiry,
    'cookies': cookies,
    'headers': headers,
    'elapsed_u': elapsed_u,
    'hacked_keywords': hacked_keywords,
    'datetime': get_date(),
    'screenshot_b64': screenshot_b64,
    'domain': domain,
    'time1': t1,
    'time2': t2,
    'time3': t3,
    'time4': t4,
    'time5': t5,
    'digest': make_hash.digest,
  })


if __name__ == '__main__':
  ret = scan("https://search.secureinfo.eu/")
  print(ret)
