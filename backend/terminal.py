#!/usr/bin/env python3

##################################################################################################################################
#    ┳╸┏━╸┏━┓┏┳┓╻┏┓╻┏━┓╺┳╸┏━┓┏━┓
#    ┃ ┣╸ ┣┳┛┃┃┃┃┃┗┫┣━┫ ┃ ┃ ┃┣┳┛
#    ╹ ┗━╸╹┗╸╹ ╹╹╹ ╹╹ ╹ ╹ ┗━┛╹┗╸
###

# Libs ###########################################################################################################################

from sys import argv
from os import popen,system
import colorama

c_green = colorama.Fore.GREEN
c_reset = colorama.Fore.RESET # + colorama.Back.RESET

c_bgblue="\033[1;44m"
c_bgmagenta="\033[1;45m"
c_blue="\033[1;34m"
c_red="\033[1;34m"
c_green="\033[1;34m"
c_yellow="\033[1;34m"
c_reset="\033[0m"

# Funcs ##########################################################################################################################

def get_term_width():
  """
  Get current terminal width thanks to 'tput'

  Input: none
  Output: integer
  """
  width = 80
  try:
    i = int(popen("tput cols").read().strip())
    width = i
  except:
    pass
  return(width)
  
def title(txt):
  """
  Print a title in full terminal length (linux, *nix) else width is 80

  Input: string
  Output: none
  """
  wdt = get_term_width() # wdt: width
  txl = len(txt) + 1
  print("\n%s> %s" % (c_bgblue,txt),end="")
  print(" " * (wdt-txl-2),end="")
  print(c_reset)

def termprint(key,value):
  """
  Print:
  key | value

  Input: tuple 
  Output: none
  """
  if type(key) == int:
    key = str(key)
  print( "%-40s | %s" % ( c_green+key+c_reset, value  ) )

def show_screenshot(img):
  """
  Show image in terminal, if terminal supports it

  Input: string (filename)
  Outile: none
  """
  system('bash backend/imgcat.sh "%s" 2>/dev/null' % img)

