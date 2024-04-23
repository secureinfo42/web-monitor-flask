from tempfile import mktemp
from os import unlink
from playwright.sync_api import sync_playwright
from base64 import b64encode

def take_screenshot(url,width=1440,height=900,device_scale_factor=1):

  # Check README.md to setup

  outfile = mktemp()
  success = 0
  with sync_playwright() as p:
    browser = p.chromium.launch()
    # page = browser.new_page()
    context = browser.new_context(viewport={'width': width, 'height': height}, device_scale_factor=device_scale_factor)
    page = context.new_page()
    # 2 minutes max
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
    import sys
    take_screenshot( sys.argv[1] )
    print("Screenshot done.")