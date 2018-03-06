#! usr/bin/python2.7

import os
import urllib
import sys
import random
import re
from skimage.io import imread


def sample_and_download_imgs(wnid, outputFolder, N):

	url = 'http://www.image-net.org/api/text/imagenet.synset.geturls?wnid='
	response = urllib.urlopen(url + wnid)
	img_urls = response.read().splitlines()

	# Select random sample from lines in text file
	print('\nSelecting '+str(N)+' sample rows...')
	random.shuffle(img_urls)
	random_img_urls = img_urls[:N]

	# Download images from sample
	print('\nDownloading images...')

	files = [int(f[:-4]) for f in os.listdir(outputFolder)]
	if files:
		print max(files)
		n = max(files) + 1
	else:
		n = 1

	print '\n'
	print n
	print '\n'
	for img_url in random_img_urls:
		try:
			img_name = outputFolder + str(n) + '.jpg'
			urllib.urlretrieve(img_url, img_name)
			n += 1
		except:
			pass


def clean_corrupted_images(outputFolder):

	print('\nLooking for corrupted images...')

	n = 0
	corrupted = 0
	for filename in os.listdir(outputFolder):
		if filename.endswith('.jpg'):
			n += 1
			try:
				img = imread(outputFolder+filename)
				if len(img.shape)<3:
					corrupted += 1
					os.remove(outputFolder+filename)	
			except:
				corrupted += 1
				os.remove(outputFolder+filename)

	print('\nRemoved '+str(corrupted)+' corrupted images')

	return n-corrupted


def main(args):

	N = int(args[0])
	wnid = args[1]
	outputFolder = args[2]

	if not outputFolder.endswith('/'):
		outputFolder += '/'
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)

	sample_and_download_imgs(wnid, outputFolder, N)
	n = clean_corrupted_images(outputFolder)

	while n<N:
		sample_and_download_imgs(wnid, outputFolder, int(1.5*(N-n)))
		n = clean_corrupted_images(outputFolder)

	print('\nFinished script. Images saved in '+outputFolder+'\n\n')


if __name__ == '__main__':
	main(sys.argv[1:])

