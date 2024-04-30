##################################################################################################################################
#    ┏━╸┏━┓┏┓╻┏━╸╻┏━╸
#    ┃  ┃ ┃┃┗┫┣╸ ┃┃╺┓
#    ┗━╸┗━┛╹ ╹╹  ╹┗━┛
###

from datetime import datetime

def get_date():
  """
  Date for filename, format is: YYYYMMDDhhmmss

  Input: none
  Output: string
  """
  current_datetime = datetime.now()
  date = current_datetime.strftime('%Y%m%d%H%M%S')
  return( date )

Headers = {
  'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36 Edg/123.0.0.0',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
  'Accept-Language': 'fr,fr-FR;q=0.8,en-US;q=0.5,en;q=0.3',
  'Accept-Encoding': 'gzip, deflate, br',
  'Connection': 'keep-alive',
  'Upgrade-Insecure-Requests': '1',
  'Sec-Fetch-Dest': 'document',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-Site': 'cross-site',
  'sec-ch-ua-platform': 'Windows',
  'sec-ch-ua': 'Google Chrome";v="123", "Chromium";v="123", "Not=A?Brand";v="24"',
  'sec-ch-ua-mobile': '?0',
  'Pragma': 'no-cache',
  'Cache-Control': 'no-cache',
}

DIGEST = "sha1"

SOCKET_TIMEOUT = 30

SSL_TIMEOUT = 30
