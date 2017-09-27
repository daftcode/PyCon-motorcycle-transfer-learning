'''
The following script is strongly based on rishabhr0y's answer to:
    https://stackoverflow.com/questions/20716842/python-download-images-from-google-image-search
'''

import os
import sys
import json
import urllib.request
from bs4 import BeautifulSoup

DIRECTORY = 'pictures_from_queries'
IMAGE_TYPE = 'ActiOn'

query = sys.argv[1:]
query = '+'.join(query)

# Search for creative commons images
url = (u'https://www.google.com/search?as_st=y&tbm=isch&as_q={}'
       '&as_epq=&as_oq=&as_eq=&cr=&as_sitesearch=&safe=images&tbs=itp'
       ':photo,ic:color,ift:jpg,sur:fc').format(query)

header = {
    u'User-Agent': u'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36'
                    ' (KHTML, like Gecko) Chrome/43.0.2357.134 Safari/537.36'}
soup = BeautifulSoup(
    urllib.request.urlopen(urllib.request.Request(url, headers=header)),
    'html.parser')


actual_images = []  # Contains the link for Large original images, type of image
for a in soup.find_all('div', {'class': 'rg_meta'}):
    link, im_type = json.loads(a.text)['ou'], json.loads(a.text)['ity']
    actual_images.append((link, im_type))

print('There are a total of {} images for query: "{}"'
      .format(len(actual_images), query))

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)
DIRECTORY = os.path.join(DIRECTORY, query.split()[0])

if not os.path.exists(DIRECTORY):
    os.mkdir(DIRECTORY)

for i, (img, im_type) in enumerate(actual_images):
    filename = os.path.join(DIRECTORY, IMAGE_TYPE + '_' + str(i) + '.jpg')
    if os.path.exists(filename):
        print('Image "{}" already exists, going further'.format(filename))
        continue

    print('Loading image to file: "{}"'.format(filename))
    try:
        req = urllib.request.Request(img, headers=header)
        raw_img = urllib.request.urlopen(req).read()
    except Exception as e:
        print('Could not load image: "{}", reason: {}'.format(img, e))
    else:
        with open(filename, 'wb') as f:
            f.write(raw_img)
