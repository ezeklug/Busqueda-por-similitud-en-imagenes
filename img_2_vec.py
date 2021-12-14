from img2vec_pytorch import Img2Vec
from PIL import Image
import glob
import json 
import os, ssl
from pyquery import PyQuery as pq

# Initialize Img2Vec with GPU
img2vec = Img2Vec(cuda=False)


with open('data.txt') as json_file:
    data = json.load(json_file)
    
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and
getattr(ssl, '_create_unverified_context', None)):
   ssl._create_default_https_context = ssl._create_unverified_context
 
base_url = "https://dr12.sdss.org"
 
def query_url(ra: float, dec: float) -> str:
   return base_url + f"/fields/raDec?ra={ra}&dec={dec}"
 
 
def img_url(path: str) -> str:
   return base_url + path

src_dir = "E:\\Proyecto GAD\\Imagenes"
count=0
iterator = glob.glob(os.path.join(src_dir, "*.jpg"))
for jpgfile in iterator:
    print(count)
    webpath = jpgfile.replace('E:\Proyecto GAD\Imagenes\imagen','')
    webpath = webpath.replace('.jpg','')
    webpath= webpath.partition('_')
    ra=webpath[0]
    dec=webpath[2]
    d = pq(query_url(ra, dec))
    webpath = d('#jpg').attr("src")        
    resource =(img_url(webpath))
    vec = str(img2vec.get_vec(Image.open(jpgfile), tensor=True))
    vec = vec.replace('tensor','')
    vec = vec.replace('(','')
    vec = vec.replace(')','')
    data['imagenes'].append({
        'path': jpgfile,
        'vector': vec,
        'web_path': resource
    })
    with open('data.txt', 'w') as outfile:
        json.dump(data,outfile)
    count+=1
