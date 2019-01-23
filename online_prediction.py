from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, MaxPooling2D,  GlobalAveragePooling2D
from keras.applications.densenet import DenseNet121
import keras
import numpy as np

inputshape =(32,32,3)
nclasses = 5

# create the base pre-trained model
base_model = DenseNet121(weights='imagenet',
                         input_shape = (32,32,3),
                         include_top=False,
                        classes=5)

# add a global spatial average pooling layer
x = base_model.output
x = GlobalAveragePooling2D()(x)
# let's add a fully-connected layer
x = Dense(1024, activation='relu')(x)
# and a logistic layer -- let's say we have 5 classes
predictions = Dense(5, activation='softmax')(x)

# this is the model we will train
mod = Model(inputs=base_model.input, outputs=predictions)
mod.load_weights("DucHau.h5")
print("Loaded model in DucHau.h5")

mod.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])
mod.summary()

from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('Elephas_App').setMaster('local[8]')
sc = SparkContext(conf=conf)

from elephas.spark_model import SparkModel

spark_model = SparkModel(mod, frequency='epoch', mode='synchronous')

image = np.load('INSA_data_images/test-img[0].npy')
image = np.expand_dims(image, axis=0)

label = spark_model.predict(image)
print('predicted label: ', label)

## Push to Minio and ES
#Imports
from minio import Minio
from minio.error import ResponseError
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

bucketName='images'

#in general
minioClient = Minio('localhost:9001', access_key='minio', secret_key='minio123', secure=False)
es = Elasticsearch([{'host':'localhost','port':9200}])

minioClient.fput_object(bucketName, 'test[0]', 'INSA_data_images/test-img[0].npy')
doc = {'image':'localhost:9001/minio/'+bucketName+'/'+'test-img[0].npy', 'labels': label.tolist()}
es.index(index='images', doc_type='npy', id=100, body=doc)
