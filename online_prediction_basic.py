from keras.models import Sequential, Model
from keras.layers import Dense, Conv2D, MaxPooling2D,  GlobalAveragePooling2D
from keras.applications.densenet import DenseNet121
import keras
import tempfile

import numpy as np
from pyspark import SparkContext, SparkConf

from minio import Minio
from minio.error import ResponseError
from elasticsearch import Elasticsearch
from elasticsearch.exceptions import ConnectionError

# create the pre-trained model
from keras.models import model_from_json 
jsonfile = open('Keras_Model_Trained/modelTrained.json', 'r')
loaded_model_json = jsonfile.read()
jsonfile.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("Keras_Model_Trained/modelTrained.h5")
print("Loaded model from disk")

opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
loaded_model.compile(optimizer=opt, loss='categorical_crossentropy', metrics = ['accuracy'])

def getLabel(labelsArray):
    class_numer = np.argmax(labelsArray)
    if class_numer == 0:
        return 'urban_area'
    if class_numer == 1:
        return 'agricultural_territory'
    if class_numer == 2:
        return 'forest'
    if class_numer == 3:
        return 'wetlands' 
    return 'surface_with_water'

# config Spark
conf = SparkConf().setAppName('Elephas_App').setMaster('local[8]')
sc = SparkContext(conf=conf)

from elephas.spark_model import SparkModel

spark_model = SparkModel(loaded_model, frequency='epoch', mode='synchronous')

images = np.load('INSA_data_images/test-img.npy')
    
predicts = spark_model.predict(images)
for i in range(20):
    print('predicted labels: ', predicts[i], ' || ', getLabel(predicts[i]))
truths = np.load('INSA_data_images/test-label.npy')


## Push to Minio and ES

bucketName='test'

minioClient = Minio('localhost:9001', access_key='minio', secret_key='minio123', secure=False)
es = Elasticsearch([{'host':'localhost','port':9200}])

for i in range(20):
    
    temporary = tempfile.NamedTemporaryFile()
    np.save(temporary, images[i])
    
    object_name = 'test-img' + str(i) + '.npy'
    
    minioClient.fput_object(bucketName, object_name, temporary.name)
    
    doc = {
        'url' : 's3a://'+ bucketName +'/'+ object_name, 
        'name':object_name,
        
        'test_label': getLabel(truths[i]),
        'predict_label': getLabel(predicts[i]),
        
        'test_array': truths[i].tolist(),
        'predict_array': predicts[i].tolist()
    }
    
    es.index(index='test', doc_type='npy', id=i, body=doc)
