#analyze_url

import requests
import config
import cert_ssl
from make_hash import md5
import web_pwnd
from bs4 import BeautifulSoup as bs
from datetime import datetime
from base64 import b64encode
from graph_timing import get_graph

import warnings
import logging
requests.packages.urllib3.disable_warnings()
warnings.filterwarnings("ignore")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


from playwright.sync_api import sync_playwright

def take_screenshot(url, output_file='screenshot.png'):
  """
  pip3 install playwright

  apt-get install libwoff1 libevent-2.1-7 libgstreamer-plugins-base1.0-0 gstreamer1.0-plugins-base \
   libharfbuzz-icu0 libenchant-2-2 libsecret-1-0 libhyphen0 libmanette-0.2-0 \
   libgles2 libgstreamer-gl1.0-0 libgstreamer-plugins-bad1.0-0


  playwright install
  """
  with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto(url)
    page.screenshot(path=output_file,full_page=True)
    browser.close()
  b64_img = b64encode( open(output_file,'rb').read() ).decode()
  return(b64_img)

def get_date():
  current_datetime = datetime.now()
  return( current_datetime.strftime('%Y-%m-%d %H:%M') )



PWND_RGX = [
  "pwn",
  r"[op][o0]?wn[e3]?d",
  r"h[a4@]ck[e3]?d",
  r"defac[e3]?d",
]

def check(txt):
  ret="No"
  for i in PWND_RGX:
    rgx = re.compile(i)
    if re.findall(rgx,txt.lower()):
      ret=f"Yes, matched: {i}"
  return(ret)

def scan(url):

  d = {}
  s = requests.session()

  r = s.get(url,verify=False,headers=config.Headers)

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
  headers = r.headers
  hacked_keywords = web_pwnd.check(r.text)
  content_md5 = md5(r.text)
  headers_md5 = md5(str(r.headers))
  header_section_md5 = md5(r.text.split('<html')[1].split('<body')[0])

  x_generator = 'Unknown'
  try: x_generator = r.headers['X-Generator']
  except: pass

  x_powered_by = 'Unknown'
  try: x_powered_by = r.headers['X-Powered-By']
  except: pass

  server = 'Unknown'
  try: server = r.headers['Server']
  except: pass

  ssl_expiry = cert_ssl.get_ssl_expiry_date(url.split('/')[2])

  # playwright install
  screenshot_b64 = take_screenshot(url)

  elapsed_u = r.elapsed.microseconds
  # timing_grah_b64 = get_graph (
  #   round(elapsed_u/100000,0) ,
  #   round(len(r.text))
  # ) 

  return({

    'url': url,
    'title': title,
    'content_md5': content_md5,
    'headers_md5': headers_md5,
    'header_section_md5': header_section_md5,
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
    # 'timing_grah_b64': timing_grah_b64,

  })

if __name__ == '__main__':

  ret = scan("https://search.secureinfo.eu/")

  print(ret)
