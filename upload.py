import os
import sys
import numpy as np
from minio import Minio
from minio.error import ResponseError
from minio.error import BucketAlreadyOwnedByYou
from minio.error import BucketAlreadyExists
from elasticsearch import Elasticsearch

#check args
if len(sys.argv) != 3:
	print "Usage: python save.py load_file_path save_directory"
	sys.exit(1)

#get args
load_file_path = sys.argv[1]
save_directory = sys.argv[2]
#minio_port = sys.argv[3]

#get list of images names
images = os.listdir(save_directory)

nb_images = len(images)

#load labels from numpy file
testLabel = np.load(load_file_path)

#connect to minio client
minioClient = Minio('localhost:9001',
                  access_key='minio',
                  secret_key='minio123',
                  secure=False)
#connect to Elasticsearch
es = Elasticsearch()

#create 'images-index' index
es.indices.create(index='images-index', ignore=400)

try:
	#create 'images' bucket
	minioClient.make_bucket("images", location="eu-west-1")
except BucketAlreadyOwnedByYou as err:
	pass
except 	BucketAlreadyExists as err:
	pass
try:
	for i in range(0,nb_images):
		#upload image i to minio
		minioClient.fput_object('images', images[i], save_directory+images[i])
		
		#index image (link to minio object) in elasticsearch
		doc = {'image':'localhost:9001/minio/images/'+images[i],'labels': testLabel[i].tolist()}
		es.index(index="images-index", doc_type="npy", id=i, body=doc)		
except ResponseError as err:
	print(err)


