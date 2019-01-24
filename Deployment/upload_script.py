from minio import Minio
from minio.error import ResponseError
from urllib3.exceptions import MaxRetryError
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError
import numpy as np
import tempfile
import time

def getLabel(labelsArray,i):
	if labelsArray[i,0]==1:
		return 'urban_area'
	if labelsArray[i,1]==1:
		return 'agricultural_territory'
	if labelsArray[i,2]==1:
		return 'forest'
	if labelsArray[i,3]==1:
		return 'wetlands'
	if labelsArray[i,4]==1:
		return 'surface_with_water'

bucketName = 'train'
bucketName2 = 'test'
indexName = 'train'
indexName2 = 'test'
nbImages = 10

minioClient = Minio('minio1:9000', access_key='minio', secret_key='minio123', secure=False)
es = Elasticsearch([{'host':'elasticsearch','port':9200}])

connectionSucceed = False
while not connectionSucceed:
	try:
		if not minioClient.bucket_exists(bucketName):
			minioClient.make_bucket(bucketName)
		if not minioClient.bucket_exists(bucketName2):
			minioClient.make_bucket(bucketName2)
		connectionSucceed = True
	except MaxRetryError as err:
		time.sleep(1)
		print(err)

connectionSucceed = False
while not connectionSucceed:
	try:
		mappings = { 'mappings': {
			'_doc' : {
				'properties':{
					'url':{'type':'text', 'enabled':False},
					'name':{'type':'text'},
					'test_label':{'type':'text'},
					'test_array': {'enabled':False},		
				}
			}
		}}
		es.indices.create(index=indexName, body=mappings, ignore=400)
		mappings = { 'mappings': {
			'_doc' : {
				'properties':{
					'url':{'type':'text', 'enabled':False},
					'name':{'type':'text'},
					'test_label':{'type':'text'},
					'predict_label':{'type':'text'},
					'test_array': {'enabled':False},
					'predict_array':{'enabled':False}		
				}
			}
		}}
		es.indices.create(index=indexName2, body=mappings, ignore=400)
		connectionSucceed = True
	except ConnectionError as err:
		time.sleep(1)
		print(err)

rgb = np.load('./INSA_data_images/test_RGB_0_10_25.npy')
labels = np.load('./INSA_data_images/test_labels_0_10_25.npy')

try:
	for i in range(0,nbImages):
		temporary = tempfile.NamedTemporaryFile()
		np.save(temporary, rgb[i])
		minioClient.fput_object(bucketName, '{0}.npy'.format(i), temporary.name)			
		doc = {
			'url':'localhost:9001/minio/'+bucketName+'/'+'{0}.npy'.format(i), 
			'name':'{0}.npy'.format(i),
			'test_label': getLabel(labels,i),
			'test_array': labels[i].tolist() 
			
		}
		es.index(index=indexName, doc_type='npy', id=i, body=doc,request_timeout=60)
except ResponseError as err:
	print(err)
