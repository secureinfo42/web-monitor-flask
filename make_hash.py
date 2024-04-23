import hashlib

def md5(mixed):
  try:
    mixed = mixed.encode()
  except:
    pass
  return(
    hashlib.md5(mixed).hexdigest()
  )