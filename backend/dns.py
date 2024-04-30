##################################################################################################################################
#   ╺┳┓┏┓╻┏━┓
#    ┃┃┃┗┫┗━┓
#   ╺┻┛╹ ╹┗━┛
###

# Libs ###########################################################################################################################

from backend import config
from os import popen
import socket

def dns_resolve(domain):

  """
  Use gethostbyaddr to resolve and reverse-lookup a domain

  Input: string
  Output: dict
  """

  host, fqdn, ip='-', '-', '-'
  try:
    fqdn = socket.getfqdn(domain)
    ip = list(set([ x[4][0] for x in socket.getaddrinfo(domain,None) ]))
    ip = ", ".join(ip)
  except:
    pass
  return({ 'host': domain, 'fqdn': fqdn, 'ip': ip })

if __name__ == '__main__':
  try:
    domain = argv[1]
    ret = scan(domain)
    print(ret)
  except:
    print("Usage: %s <domain>" % argv[0])
    exit()
