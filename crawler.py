import os
import sys
import urllib2
import requests
import cv2
import io
import numpy as np
from colordescriptor import ColorDescriptor
from PIL import Image 
from bs4 import BeautifulSoup
from flask import Flask, render_template, request, redirect
from StringIO import StringIO
from datetime import datetime
from elasticsearch import Elasticsearch
import re
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

cd = ColorDescriptor((4, 8, 4))
global count
count =0;
def download_image(url, num):
   	try:
		fd = urllib2.urlopen(str(url))
		image_file = StringIO(fd.read())
		im = Image.open(image_file)
		#print(im)
		image =np.array(im)
		#print(image)
		resized_image = cv2.resize(image, (192, 256),interpolation=cv2.INTER_AREA)
		#print(resized_image)
		#image = cv2.cvtColor(resized_image, cv2.COLOR_BGR2GRAY)
		features = cd.describe(resized_image)
		doc1 = {
			"url": str(url), 'feature': str(features), "timestamp": datetime.now(),
		}
		#print (len(doc['feature']))
		ind=es.index(index='image', doc_type='img', id=num, body=doc1)
		print(ind['_shards']['successful'])
		#print features
	
	except ValueError:
        	print("Invalid URL !")
	except:
		print("Unknown Exception" + str(sys.exc_info()[0]))

feature=[]
doc = {
    'size' : 10000,
    'query': {
        'match_all' : {}
    }
}
#extracting first 10000 webpage links
res = es.search(index="url", doc_type='link', body=doc,scroll='1m') 
scroll = res['_scroll_id']
#extracting 10000 to 20000 webpage links
res2 = es.scroll(scroll_id = scroll, scroll = '1m')
for doc in res['hits']['hits']:
	url=doc['_source']['link']
	#print("mainurl : ")
	#print(url)
	links=[]
	html_page = urllib2.urlopen(url)
    	soup = BeautifulSoup(html_page,"lxml")
    	for link in soup.findAll('a', attrs={'href': re.compile("^http://")}):
        	links.append(link.get('href'))
	links.append(url)
for inlink in links:
	_url=inlink
	#print(_url)
    	try:
        	
        	code = requests.get(_url)
        	text = code.text
        	soup1 = BeautifulSoup(text)
        	for img in soup1.findAll('img'):
			#print(img)
            		count += 1
            		if (img.get('src'))[0:4] == 'http':
                		src = img.get('src')
            		else:
                		src = urljoin(_url, img.get('src'))
	    		question_mark = src.find("?")
	    		src = src[:question_mark]
	    		print(src)
            		download_image(src, count)
    	except requests.exceptions.HTTPError as error:
        	print(str(error))




