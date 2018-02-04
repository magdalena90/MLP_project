
import os
import sys
import tensorflow as tf
from scipy.misc import imsave, imread, imresize

def load_image(path):
    img = imread(path)
    
	# crop image from center
    short_edge = min(img.shape[:2])
    yy = int((img.shape[0] - short_edge) / 2)
    xx = int((img.shape[1] - short_edge) / 2)
    crop_img = img[yy : yy + short_edge, xx : xx + short_edge]
    
	# resize to 224, 224
    img = imresize(crop_img, [224, 224])
    
	# desaturate image
    return (img[:,:,0] + img[:,:,1] + img[:,:,2]) / 3.0


def main(args):
	inputFolder = args[0]
	outputFolder = args[1]

	if not inputFolder.endswith('/'):
		inputFolder += '/'
	if not outputFolder.endswith('/'):
		outputFolder += '/'
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)

	allFiles = os.listdir(inputFolder)
	imgFiles = [f for f in allFiles if f.endswith('.jpg')]

	img_gray = load_image(inputFolder+imgFiles[0]).reshape(1, 224, 224, 1)

	with open('colorize.tfmodel', mode='rb') as f:
		fileContent = f.read()

	graph_def = tf.GraphDef()
	graph_def.ParseFromString(fileContent)
	grayscale = tf.placeholder('float', [1, 224, 224, 1])
	#tf.import_graph_def(graph_def, input_map={ "grayscale": grayscale }, name='')
	inferred_rgb, = tf.import_graph_def(graph_def, input_map={'grayscale': grayscale },
		                                return_elements=['inferred_rgb:0'])

	with tf.Session() as sess:
		#inferred_rgb = sess.graph.get_tensor_by_name("inferred_rgb:0")
		inferred_batch = sess.run(inferred_rgb, feed_dict={ grayscale: img_gray })
		imsave(outputFile+img_gray, inferred_batch[0])
		print "saved shark-color.jpg"


if __name__ == '__main__':
	main(sys.argv[1:])

