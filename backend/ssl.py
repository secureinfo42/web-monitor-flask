##################################################################################################################################
#    ┏━┓┏━┓╻      
#    ┗━┓┗━┓┃      
#    ┗━┛┗━┛┗━╸    
###

# Libs ###########################################################################################################################

from backend import config
from datetime import datetime
from time import sleep
from os import popen
import OpenSSL
import re
import socket
import ssl
import warnings
import logging

warnings.filterwarnings("ignore")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

# Funcz ##########################################################################################################################

def _get_altnames(cert):
  """
  Get SSL alternate names certificate validity in a list 

  Input: object (cert)
  Output: list
  """

  altnames = []
  if 'subjectAltName' in cert:
    for i in cert['subjectAltName']:
      if i[0] == "DNS":
        altnames.append( i[1] )
  return(altnames)

def get_ssl_infos(hostname,port=443):
  """
  Get SSL informations: commonName, Issuer_commonName, caIssuers, notBefore,
  notAfter, is_expired, version, serialNumber, subjectAltNames

  Input: tuple (hostname,port)
  Output: dict
  """

  res = {
    'commonName'    : '-',
    'Issuer_commonName' : '-',
    'caIssuers'     : '-',
    'notBefore'     : '-',
    'notAfter'      : '-',
    'is_expired'    : '-',
    'version'       : '-',
    'serialNumber'    : '-',
    'subjectAltNames'    : '-',
  }

  context = ssl.create_default_context()

  with socket.create_connection((hostname, int(port))) as sock:
    sock.settimeout(config.SOCKET_TIMEOUT)
    try:
      with context.wrap_socket(sock, server_hostname=hostname) as ssl_socket:
        ssl_socket.settimeout(config.SSL_TIMEOUT)
        cert = ssl_socket.getpeercert()
        current_time = datetime.now()
        not_after = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
        subjectAltNames = _get_altnames(cert)

        is_expired = "True"
        if current_time < not_after:
          is_expired = "False"

        res.update({ 'commonName'        : cert["subject"][0][0][1]   })
        res.update({ 'Issuer_commonName' : cert["issuer"] [1][0][1]   })
        res.update({ 'caIssuers'         : cert["caIssuers"] [0]      })
        res.update({ 'notBefore'         : cert["notBefore"]          })
        res.update({ 'notAfter'          : cert["notAfter"]           })
        res.update({ 'is_expired'        : is_expired                 })
        res.update({ 'version'           : cert["version"]            })
        res.update({ 'serialNumber'      : cert["serialNumber"]       })
        res.update({ 'subjectAltNames'   : subjectAltNames            })

    except ssl.SSLCertVerificationError as e:
      print("Error: problem while gathering certificate informations")

  return(res)

# def get_openssl(hostname, port=443):
#   if not re.findall(r'^[a-zA-Z0-9\._-]{1,64}$',hostname):
#     return("Bad hostname")
#   if not re.findall(r'^[0-9]{3,5}$',str(port)):
#     return("Bad port")
#   cmd = "true|openssl s_client -connect '%s:%s' -showcerts <<< /dev/null 2>/dev/null|awk -F'NotAfter:' '/NotAfter:/{ print $2 }';#" % (hostname,port)
#   ret = popen(cmd).read().strip()
#   return(ret)


if __name__ == '__main__':
  try:
    hostname = argv[1]
    port = int(argv[2])
    ret = get_ssl_infos(hostname,port)
    print(ret)
  except:
    print("Usage: %s <hostname> <port>" % argv[0])
    exit()
