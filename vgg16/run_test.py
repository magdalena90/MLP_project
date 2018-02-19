
import os
import sys
import tensorflow as tf
import skimage.transform
from skimage.io import imsave, imread


def load_image(path):
  img = imread(path)
    
  img = img[:,int(img.shape[1]/2):,:]

	# crop image from center
  short_edge = min(img.shape[:2])
  yy = int((img.shape[0] - short_edge) / 2)
  xx = int((img.shape[1] - short_edge) / 2)
  img = img[yy : yy + short_edge, xx : xx + short_edge]

  # resize to 224, 224
  img = skimage.transform.resize(img, (224, 224), mode='constant')
    
	# desaturate image
  img = (img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3.0

  return img


def run_model(inputFolder, outputFolder):

	# Get files
	allFiles = os.listdir(inputFolder)
	imgFiles = [f for f in allFiles if f.endswith('.jpg')]
	n = len(imgFiles)

	imgs = []
	for imgFile in imgFiles:
		img = load_image(inputFolder+imgFile).reshape(224, 224, 1)
		imgs.append(img)

	# Create variables
	with open('colorize.tfmodel', mode='rb') as f:
		fileContent = f.read()

	graph_def = tf.GraphDef()
	graph_def.ParseFromString(fileContent)
	grayscale = tf.placeholder('float', [n, 224, 224, 1])
	inferred_rgb, = tf.import_graph_def(graph_def, input_map={'grayscale': grayscale}, return_elements=['inferred_rgb:0'])

	# Run model
	with tf.Session() as sess:
		inferred_batch = sess.run(inferred_rgb, feed_dict={grayscale: imgs})

		for i in range(len(inferred_batch)):
			imsave(outputFolder+imgFiles[i], inferred_batch[i])


def main(args):
	inputFolder = args[0]
	outputFolder = args[1]

	# Hide TensorFlow low level warning
	os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

	# Folders checks
	if not inputFolder.endswith('/'):
			inputFolder += '/'
	if not outputFolder.endswith('/'):
			outputFolder += '/'
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)

	# Run model
	run_model(inputFolder, outputFolder)


if __name__ == '__main__':
 	main(sys.argv[1:])
