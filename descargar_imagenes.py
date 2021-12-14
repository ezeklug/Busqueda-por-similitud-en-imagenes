import urllib.request as ur
from pyquery import PyQuery as pq
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)): ssl._create_default_https_context = ssl._create_unverified_context

base_url = "https://dr12.sdss.org"
 
def query_url(ra: float, dec: float) -> str:
   return base_url + f"/fields/raDec?ra={ra}&dec={dec}"
 
 
def img_url(path: str) -> str:
   return base_url + path
 
 
# Downloads an image of the celestial sphere in the Ra,Dec pos
# out_name is the output name of the file
def download_image(ra: float, dec: float, out_name: str):
   try:
      print(f"ra: {ra}, dec: {dec}")
      response = ur.urlopen(query_url(ra,dec))
   except ur.HTTPError as e:
      print('HTTPError: {}'.format(e.code))
      return dec+25
   else:       
      d = pq(query_url(ra, dec))
      path = d('#jpg').attr("src")
      if (path):
         print(f"Downloading imagen{ra}_{dec}.jpg")
         resource = ur.urlopen(img_url(path))
         with open(out_name, "wb") as f:
            f.write(resource.read())
         return dec+0.2
      else: 
         print(f"imagen{ra}_{dec}.jpg Doesn't Exist")
         return dec+25

count=0
i=0
while i < 40:
    j=0.2
    i+=0.2
    while j<40:
        count+=1
        j=download_image(i, j, f"imagen{i}_{j}.jpg")