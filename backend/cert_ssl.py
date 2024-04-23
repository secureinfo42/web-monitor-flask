import ssl
import socket
from datetime import datetime
from os import popen
import re

import warnings
import logging
warnings.filterwarnings("ignore")
logging.getLogger("scapy.runtime").setLevel(logging.ERROR)


def get_openssl(hostname, port=443):
    if not re.findall(r'^[a-zA-Z0-9\._-]{1,64}$',hostname):
        return("Bad hostname")
    if not re.findall(r'^[0-9]{3,5}$',str(port)):
        return("Bad hostname")
    cmd = "true|openssl s_client -connect '%s:%s' -showcerts <<< /dev/null 2>/dev/null|awk -F'NotAfter:' '/NotAfter:/{ print $2 }';#" % (hostname,port)
    ret = popen(cmd).read().strip()
    return(ret)

def get_ssl_expiry_date(hostname, port=443):
    context = ssl.create_default_context()
    context.check_hostname = False
    # context.verify_mode = ssl.CERT_NONE

    try:
        with socket.create_connection((hostname, port)) as sock:
            with context.wrap_socket(sock, server_hostname=hostname) as ssock:
                cert = ssock.getpeercert()
                return datetime.strptime(cert['notAfter'], '%b %d %H:%M:%S %Y %Z')
    except:
        return( get_openssl(hostname,port) )

if __name__ == '__main__':
    # Exemple d'utilisation
    hostname = 'bibliotheques-numeriques.defense.gouv.fr'
    expiry_date = get_ssl_expiry_date(hostname)
    print("Le certificat SSL expire le :", expiry_date)
