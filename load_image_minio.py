from pyspark import SparkContext, SparkConf
import numpy as np

from skimage.color import rgb2gray
from skimage.filters import sobel
from skimage.segmentation import felzenszwalb
from skimage.segmentation import mark_boundaries
from skimage.util import img_as_float

import cv2
#from matplotlib import pyplot as plt

records = [{'_source': {'url': 's3a://test/test-img7.npy',
   'name': 'test-img7.npy',
   'test_label': 'forest',
   'predict_label': 'forest',
   'test_array': [0.0, 0.0, 1.0, 0.0, 0.0],
   'predict_array': [0.00601671077311039,
    0.047392837703228,
    0.5142027735710144,
    0.06994199752807617,
    0.013775604777038097]}}
]

conf = SparkConf()
sc = SparkContext(conf=conf)

b1 = sc.textFile(records[0]['_source']['url'])

print("Image")
image = b1.collect()
print(image)

# plt.imshow(image, cmap='gray')
# plt.show()

