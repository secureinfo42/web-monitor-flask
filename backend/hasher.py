##################################################################################################################################
#    ╻ ╻┏━┓┏━┓╻ ╻┏━╸┏━┓
#    ┣━┫┣━┫┗━┓┣━┫┣╸ ┣┳┛
#    ╹ ╹╹ ╹┗━┛╹ ╹┗━╸╹┗╸
###

# Libs ###########################################################################################################################

from hashlib import md5,sha1,sha256,sha512
from backend import config

def gethash(data):
  """
  Get SSL alternate names certificate validity in a list 

  Input: string
  Output: string (hexa)
  """

  try:
    data = data.encode()
  except:
    pass

  if config.DIGEST.lower() == "md5"    : return( md5(data).hexdigest()    )
  if config.DIGEST.lower() == "sha1"   : return( sha1(data).hexdigest()   )
  if config.DIGEST.lower() == "sha256" : return( sha256(data).hexdigest() )
  if config.DIGEST.lower() == "sha512" : return( sha512(data).hexdigest() )
