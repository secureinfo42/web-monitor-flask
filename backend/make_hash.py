import hashlib

digest = 'SHA1'

def make_hash(mixed):
  try:
    mixed = mixed.encode()
  except:
    pass
  return(hashlib.sha1(mixed).hexdigest())
  # return(hashlib.sha256(mixed).hexdigest())