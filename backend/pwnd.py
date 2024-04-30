##################################################################################################################################
#    ┏━┓╻ ╻┏┓╻╺┳┓
#    ┣━┛┃╻┃┃┗┫ ┃┃
#    ╹  ┗┻┛╹ ╹╺┻┛
###

import re

PWND_RGX = [
  r"[op][o0]?wn[e3]?d",
  r"h[a4@]ck[e3]?d",
  r"d[e3]f[a4@]c[e3]?d",
]

def check(txt):
  """
  Check if text contain a regex

  See: pwnd.PWND_RGX

  Input: string
  Output: string
  """  
  global PWND_RGX
  ret="No"
  for i in PWND_RGX:
    rgx = re.compile(i)
    if re.findall(rgx,txt.lower()):
      ret=f"Yes, matched regex: {i}"
  return(ret)