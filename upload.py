import os
import sys
import numpy as np
from minio import Minio
from minio.error import ResponseError
from minio.error import BucketAlreadyOwnedByYou
from minio.error import BucketAlreadyExists

#check args
if len(sys.argv) != 4:
	print "Usage: python save.py load_file_path save_directory minio_port"
	sys.exit(1)

#get args
load_file_path = sys.argv[1]
save_directory = sys.argv[2]
minio_port = sys.argv[3]

images = os.listdir(save_directory)
nb_images = len(images)

print nb_images


testLabel = np.load(load_file_path)

minioClient = Minio('localhost:'+minio_port,
                  access_key='minio',
                  secret_key='minio123',
                  secure=False)

try:
	#create 'images' bucket
	minioClient.make_bucket("images", location="eu-west-1")
except BucketAlreadyOwnedByYou as err:
	pass
except 	BucketAlreadyExists as err:
	pass
try:
	for i in range(0,nb_images):
		metadata = {'labels':testLabel[i]}
		minioClient.fput_object('images', images[i], save_directory+images[i],metadata=metadata)
except ResponseError as err:
	print(err)

#visualize image information
for image in images:
	info = minioClient.stat_object('images',image)
	print(info)
