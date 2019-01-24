from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
import keras
import numpy as np

testLabel=np.load('INSA_data_images/CLEAN_test_labels_0_10_25.npy')
testRGB = np.load('INSA_data_images/CLEAN_test_RGB_0_10_25.npy')
#trainLabel= np.load('INSA_data_images/train_labels_0_10_25.npy')
#trainRGB = np.load('INSA_data_images/train_RGB_0_10_25.npy')


#LOAD KERAS MODEL
jsonfile = open('Keras_Model_Trained/modelTrained.json', 'r')
loaded_model_json = jsonfile.read()
jsonfile.close()
loaded_model = model_from_json(loaded_model_json)
loaded_model.load_weights("Keras_Model_Trained/modelTrained.h5")
print("Loaded model from disk")

loaded_model.summary()

opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
mod.compile(optimizer=opt, loss='categorical_crossentropy', metrics = ['accuracy'])

indices = np.random.randint(1000, size=1000)

# DONNEES NON TRAITEES
data = testRGB[indices]
target = testLabel[indices]
xtrain = data
ytrain = target
xtest = testRGB[0:100]
ytest = testLabel[0:100]

# SPARK
from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('Elephas_App').setMaster('local[8]')
sc = SparkContext(conf=conf)

# ELEPHAS
from elephas.utils.rdd_utils import to_simple_rdd

rdd = to_simple_rdd(sc, xtrain, ytrain)

from elephas.spark_model import SparkModel

spark_model = SparkModel(loaded_model, frequency='epoch', mode='synchronous')
spark_model.fit(rdd, batch_size=32, epochs=10, verbose=0,validation_split=0.1)

scoreT =spark_model.master_network.evaluate(xtest, ytest, verbose=1)
print('accuracy ', scoreT)
