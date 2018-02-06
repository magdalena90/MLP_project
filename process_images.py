#! usr/bin/python2.7

import sys
import os
import numpy as np
from scipy.misc import imresize, imread, imsave


def resize_img(img, height, width):

	height_ratio = float(img.shape[0])/height
	width_ratio = float(img.shape[1])/width
	resize_ratio = height_ratio/width_ratio

	# Crop img so resize doesn't stretch it (make resize_ratio=1)
	if height_ratio < width_ratio:
		cropped_width = int(height_ratio * width)
		start = (img.shape[1]-cropped_width)/2
		end = start + cropped_width
		img_cropped = img[:, start:end, :]
	else:
		cropped_height = int(width_ratio * height)
		start = (img.shape[0]-cropped_height)/2
		end = start + cropped_height
		img_cropped = img[start:end, :, :]

	# Resize
	img_resized = imresize(img_cropped, [height, width])

	return img_resized


def color2grayscale(img):

	gray = np.average(img, axis=2, weights=[0.299,0.587,0.114])[:,:,np.newaxis]
	gray, _ = np.broadcast_arrays(gray, img)

	return gray


def preprocess_img(img, height, width):

	color = resize_img(img, height, width)
	grayscale = color2grayscale(color)

	return color, grayscale


def load_img(path, height, width):

	img = imread(path).astype(np.float)

	if (img.shape[0] > height and img.shape[1] > width):
		img_A, img_B = preprocess_img(img, height, width)
		return [img_A, img_B]
	else:
		return None


def save_img(path, img_A, img_B, train_or_test):
	if train_or_test == 'train':
		img = np.concatenate((img_A, img_B), axis=1)
	else:
		img = img_B
	imsave(path, img)


def main(args):
	inputFolder = args[0]
	outputFolder = args[1]
	max_n_imgs = int(args[2])
	height = int(args[3])
	width = int(args[4])
	train_or_test = args[5]

	if not inputFolder.endswith('/'):
		inputFolder += '/'
	if not outputFolder.endswith('/'):
		outputFolder += '/'
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)

	allFiles = os.listdir(inputFolder)
	imgFiles = [f for f in allFiles if f.endswith('.jpg')]

	print('\nProcessing images...')
	skipped = 0
	for imgFile in imgFiles[:max_n_imgs]:
		try:
			img = load_img(inputFolder + imgFile, height, width)

			if img is None:
				skipped += 1
			else:
				save_img(outputFolder + imgFile, img[0], img[1], train_or_test)
		except:
			skipped += 1
	print('\nSkipped ' + str(skipped) + ' images because of size')
	print('\nFinished script. New images saved in '+outputFolder+'\n\n')


if __name__ == '__main__':
	main(sys.argv[1:])
