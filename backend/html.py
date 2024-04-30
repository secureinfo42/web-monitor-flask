#!/usr/bin/env python3

##################################################################################################################################
#    ┳╸┏━╸┏━┓┏┳┓╻┏┓╻┏━┓╺┳╸┏━┓┏━┓
#    ┃ ┣╸ ┣┳┛┃┃┃┃┃┗┫┣━┫ ┃ ┃ ┃┣┳┛
#    ╹ ┗━╸╹┗╸╹ ╹╹╹ ╹╹ ╹ ╹ ┗━┛╹┗╸
###

# Libs ###########################################################################################################################

from sys import argv
from datetime import datetime
from os import mkdir, stat

# Funcs ##########################################################################################################################

def write_table(title, table, html_class={'table': '', 'th': '', 'td': ''}):
  """
  Write a HTML table

  Input: 
  Output: string
  """

  htmldata  = '<h3>%s</h3><table border=1 class="%s">' % (title,html_class['table'])
  for key,value in table.items():
    htmldata += "<tr>"
    htmldata += '<th class="%s">%s</th>' % (html_class['th'] , key)
    htmldata += '<td class="%s">%s</th>' % (html_class['td'] , value)
    htmldata += "</tr>"
  htmldata += "</table>"

  return(htmldata)
  

def write_div(title, values, html_class={'table': '', 'th': '', 'td': '', 'div': ''}):
  """
  Write a HTML table surrounded by a div

  Input: 
  Output: string
  """

  htmldata  = '<h3>%s</h3>' % (title)
  htmldata += '<div class="%s">' % (html_class['div'])
  htmldata += '<table border=1 class="%s">' % (html_class['table'])
  for key,value in values:
    # print(key,value)
    htmldata += "<tr>"
    htmldata += '<th class="%s">%s</th>' % (html_class['th'] , key)
    htmldata += '<td class="%s">%s</th>' % (html_class['td'] , value[1])
    htmldata += "</tr>"
  htmldata += "</table>"
  htmldata += "</div>"

  return(htmldata)
  

def h2(title):

 return('<br/><h2>%s</h2><hr>' % (title))
 
  
def save_report(htmldata,domain,current_date):

  for folder in ["reports",f"reports/{domain}",f"reports/{domain}/static"]:
    try:    stat(folder)
    except: mkdir(folder)

  outfile = "reports/%s/%s.html" % (domain,current_date)
  open(outfile,"w").write(htmldata)

  try:
      stat("reports/%s/static/chart.js" % domain)
  except:
      js = open("static/chart.js","r").read()
      open("reports/%s/static/chart.js" % domain,"w").write(js)

   
