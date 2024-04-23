import re

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