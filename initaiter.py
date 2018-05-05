
from datetime import datetime
from elasticsearch import Elasticsearch
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
doc = {
			"link": 'https://prateekvjoshi.com/2016/03/01/how-to-read-an-image-from-a-url-in-opencv-python/', "timestamp": datetime.now(),
		}
res=es.index(index='url', doc_type='link', id=1, body=doc)
#es.indices.delete(index='image', ignore=[400, 404])
