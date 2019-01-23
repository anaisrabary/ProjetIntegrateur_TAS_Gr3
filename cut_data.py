import numpy as np

testLabel= np.load('INSA_data_images/test_labels_0_10_25.npy')
testRGB = np.load('INSA_data_images/test_RGB_0_10_25.npy')

for image in testRGB:
    np.save('test[]')
