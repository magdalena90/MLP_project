#! usr/bin/python2.7

import sys
import os
import numpy as np
from scipy.misc import imresize, imread, imsave


def cut_and_save_imgs(img, n, outputFolder):
	n_imgs = img.shape[0]/256
	for n_img in range(n_imgs):
		new_img = img[256*n_img:256*(n_img+1), :, :]
		imsave(outputFolder+str(n)+'.png', new_img)
		n += 1

	return n_imgs


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
	imgFiles = [f for f in allFiles if f.endswith('.png')]

	print('\nProcessing images...')
	n_tot = 0
	for imgFile in imgFiles:
		try:
			img = imread(inputFolder+imgFile).astype(np.float)
			n = cut_and_save_imgs(img, n_tot, outputFolder)
			n_tot += n
		except:
			pass

	print('\nFinished script. New images saved in '+outputFolder+'\n\n')


if __name__ == '__main__':
	main(sys.argv[1:])
