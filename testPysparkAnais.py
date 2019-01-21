from keras.models import Sequential
from keras.layers import Dense, Conv2D, MaxPooling2D, Dropout, Flatten
import keras
import numpy as np

testLabel=np.load('INSA_data_images/test_labels_0_10_25.npy')
testRGB = np.load('INSA_data_images/test_RGB_0_10_25.npy')
trainLabel= np.load('INSA_data_images/train_labels_0_10_25.npy')
trainRGB = np.load('INSA_data_images/train_RGB_0_10_25.npy')


def createModel(inputshape,nClasses):
#See here for info : 
# https://www.learnopencv.com/image-classification-using-convolutional-neural-networks-in-keras/ 
# empilement de Conv layers puis de Max pooling layers.
# Dropout permet d'éviter l'overfitting
# A la fin, on a une fully connected layer (Dense) suivie d'une sopftmax layer
    model = Sequential()
    model.add(Conv2D(32, (3,3), padding='same',activation='relu', input_shape=inputshape))
    # 32 filters/kernels with (3*3) size window.
    model.add(Conv2D(32, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25)) # 0.25 : dropout ratio
    
    model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Conv2D(64, (3,3), padding='same', activation='relu'))
    model.add(Conv2D(64, (3,3), activation='relu'))
    model.add(MaxPooling2D(pool_size=(2,2)))
    model.add(Dropout(0.25))
    
    model.add(Flatten())
    model.add(Dense(512, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(nClasses, activation='softmax'))
    
    return model

# 6 Conv layze, 1 fully-connected layer
inputshape =(32,32,3)
nclasses = 5
mod = createModel(inputshape, nclasses)
mod.summary()

#KERAS WORKFLOW 

opt = keras.optimizers.rmsprop(lr=0.0001, decay=1e-6)
mod.compile(optimizer=opt, loss='categorical_crossentropy', metrics = ['accuracy'])

indices = np.random.randint(1000, size=1000)

# DONNEES NON TRAITEES
data = trainRGB[indices]
target = trainLabel[indices]
xtrain = data
ytrain = target
xtest = testRGB
ytest = testLabel

import os
os.environ['PYSPARK_PYTHON'] = 'Users\anais\AppData\Local\Programs\Python\Python36'

from pyspark import SparkContext, SparkConf

conf = SparkConf().setAppName('Elephas_App').setMaster('local[8]')
sc = SparkContext(conf=conf)

from elephas.utils.rdd_utils import to_simple_rdd

rdd = to_simple_rdd(sc, xtrain, ytrain)

from elephas.spark_model import SparkModel

spark_model = SparkModel(mod, frequency='epoch', mode='synchronous')
spark_model.fit(rdd, batch_size=32, epochs=10, verbose=0,validation_split=0.1)









