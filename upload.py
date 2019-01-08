from minio import Minio
from minio.error import ResponseError
from minio.error import BucketAlreadyOwnedByYou
from minio.error import BucketAlreadyExists

minioClient = Minio('localhost:9001',
                  access_key='minio',
                  secret_key='minio123',
                  secure=False)

try:
	#create 'images' bucket
       minioClient.make_bucket("images", location="eu-west-1")
except BucketAlreadyOwnedByYou as err:
       pass
except BucketAlreadyExists as err:
       pass
except ResponseError as err:
       raise
else:
        #put
        try:
               minioClient.fput_object('images', 'pink.jpeg', './images/pink.jpeg')
        except ResponseError as err:
               print(err)
