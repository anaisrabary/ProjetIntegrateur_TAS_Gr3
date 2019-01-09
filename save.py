import sys
import numpy as np

#check args
if len(sys.argv) != 4:
	print "Usage: python save.py load_file_path save_directory nb_images"
	sys.exit(1)

#get args
load_file_path = sys.argv[1]
save_directory = sys.argv[2]
nb_images = sys.argv[3]

#load images from numpy file
images = np.load(load_file_path)

#save each image to save directory
for i in range(0,int(nb_images)):
	np.save(save_directory+"{0}.npy".format(i),images[i])
