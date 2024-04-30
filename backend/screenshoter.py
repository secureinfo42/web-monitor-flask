##################################################################################################################################
#    ┏━┓┏━┓╻      
#    ┗━┓┗━┓┃      
#    ┗━┛┗━┛┗━╸    
###

# Libs ###########################################################################################################################

from tempfile import mktemp
from os import unlink
from playwright.sync_api import sync_playwright
from base64 import b64encode,b64decode

def take_screenshot(url,width=1440,height=900,device_scale_factor=1):

  """
  Take screenshot of remote URL, default size 1440x900, scaled 1x
  and return base64 of picture

  Setup:
  $ pip3 install playwright
  $ sudo apt-get -y install libwoff1 libevent-2.1-7 libgstreamer-plugins-base1.0-0 gstreamer1.0-plugins-base \
    libharfbuzz-icu0 libenchant-2-2 libsecret-1-0 libhyphen0 libmanette-0.2-0 \
    libgles2 libgstreamer-gl1.0-0 libgstreamer-plugins-bad1.0-0
  $ playwright install


  Input: string,int,int,int
  Output: string
  """

  outfile = mktemp()
  success = 0
  with sync_playwright() as p:
    browser = p.chromium.launch()

    # Set virtual window size
    context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=device_scale_factor)
    page = context.new_page()

    # 2 minutes max in 12 tries
    for i in range(12):
      try:
        page.goto(url)
      except:
        sleep(10)
      break
    page.screenshot(path=outfile,full_page=False)
    browser.close()

  b64_img = b64encode( open(outfile,'rb').read() ).decode()
  unlink(outfile)
  return(b64_img)

if __name__ == '__main__':
    from sys import argv
    try:
      url,outfile = argv[1],argv[2]
    except:
      print("Usage: %s <url> <out.png>" % argv[0])
      exit()
    b64data = take_screenshot( url )
    open( outfile , "wb" ).write( b64decode(b64data) )
    print("Screenshot saved to : '%s'" % outfile)

