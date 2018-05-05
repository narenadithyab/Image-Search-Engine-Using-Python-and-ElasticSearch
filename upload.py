import os
from flask import Flask, render_template, request
from PIL import Image 
import numpy as np
import cv2
import hashlib
from colordescriptor import ColorDescriptor
from elasticsearch import Elasticsearch

app = Flask(__name__)
cd = ColorDescriptor((4, 8, 4))
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

@app.route('/')
def main():
    return render_template("webproj.html")

@app.route("/upload", methods=['POST'])
def upload_file():
	if request.method == 'POST':
		
      		f = request.files['fileToUpload']
		#print(f)
		sfname = 'images/'+str(f.filename)
		#return 'file uploaded successfully'
		f.save(sfname)
		im = Image.open(sfname)
		#print(im)
		image =np.array(im)
		#print(image)
		resized_image = cv2.resize(image, (192, 256),interpolation=cv2.INTER_AREA)
		features = cd.describe(resized_image)
		#print(features)
		doc = {
			"query": {'match':{ "feature": str(features)}}
		}
		#print(doc)
		res=es.search(index='image',doc_type='img', body=doc)
		#print(res['hits'])
		k=0
		f = open('/home/narenadithya/Image-Crawler-master/templates/search.html', 'r')
		myfile = open('/home/narenadithya/Image-Crawler-master/templates/search1.html', 'w')
		for line in f.readlines():
			myfile.write(line)
		f.close()		
		for i in res['hits']['hits']:
			if k==10:
				break;
			myfile.write('<tr><td><a href =\"{}\">{}</a></td><td><img src=\"{}\" style=\"width:100px;height:150px;\"></td><td>{}</td></tr>'.format(i['_source']['url'],i['_source']['url'],i['_source']['url'],i['_score']))
			#print('{} {}'.format(i['_source']['url'],i['_score']))
			print('<a href =\"{}\">{}</a> <img src=\"{}\" style=\"width:100px;height:150px;\"><br>'.format(i['_source']['url'],i['_source']['url'],i['_source']['url']))
			k=k+1
		myfile.close()
		#return 'file uploaded successfully'
      	#return 'file uploaded successfully'

	return render_template("search1.html")

if __name__ == '__main__':
   app.run()
