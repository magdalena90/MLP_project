#! usr/bin/python2.7

import os
import urllib
import tarfile
import sys
import random
import re
from skimage.io import imread


def download_url_list(tarFile, oldUrlsFile, newUrlsFile):

	# Download tar file from ImageNet
	if (not os.path.isfile(tarFile) and not os.path.isfile(newUrlsFile)):
		print('\nDownloading list of urls...')
		tarUrl = 'http://image-net.org/imagenet_data/urls/imagenet_fall11_urls.tgz'
		urllib.urlretrieve (tarUrl, tarFile)
	elif os.path.isfile(tarFile):
		print('\nDecompressed tar file already exists, skipping download')
	else:
		print('\nTar file with url list aready exists, skipping download')

	# Decompress tar file
	if not os.path.isfile(newUrlsFile):
		print('\nDecompressing tar file...')
		tar = tarfile.open(tarFile)
		tar.extractall(path='Images')
		tar.close()
		os.rename(oldUrlsFile, newUrlsFile)
	else:
		print('\ntar file already decompressed, skipping decompression')


def sample_and_download_imgs(newUrlsFile, N):

	# Select random sample from lines in text file
	print('\nSelecting '+str(N)+' sample rows...')
	num_lines = sum(1 for line in open(newUrlsFile, 'r'))
	random_lines = random.sample(xrange(1, num_lines), N)
	imgIdRegex = re.compile('^\S*')
	imgUrlRegex = re.compile('http[^ ]+')

	# Download images from sample
	print('\nDownloading images...')
	n = 0
	with open(newUrlsFile) as f:
		for line in f:
			n += 1
			if n in random_lines:
				imgId = 'Images/'+imgIdRegex.findall(line)[0]+'.jpg'
				imgUrl = imgUrlRegex.findall(line)[0]
				try:
					urllib.urlretrieve(imgUrl, imgId)
				except:
					pass


def clean_corrupted_images():

	print('\nLooking for corrupted images...')

	n = 0
	corrupted = 0
	for filename in os.listdir('Images/'):
		if filename.endswith('.jpg'):
			n += 1
			try:
				img = imread('Images/'+filename)
				if len(img.shape)<3:
					corrupted += 1
					os.remove('Images/'+filename)	
			except:
				corrupted += 1
				os.remove('Images/'+filename)

	print('\nRemoved '+str(corrupted)+' corrupted images')

	return n-corrupted


def remove_url_files(removeTar, tarFile, removeFullList, newUrlsFile):

	if removeTar=='True' and os.path.isfile(tarFile):
		print('\nRemoving tar file')
		os.remove(tarFile)

	if removeFullList=='True' and os.path.isfile(newUrlsFile):
		print('\nRemoving full url list file')
		os.remove(newUrlsFile)


def main(args):

	N = int(args[0])
	outputFolder = args[1]
	removeTar = args[2]
	removeFullList = args[3]

	if not outputFolder.endswith('/'):
		outputFolder += '/'
	if not os.path.exists(outputFolder):
		os.makedirs(outputFolder)

	tarFile = outputFolder + '_tarFile.tgz'
	oldUrlsFile = outputFolder + 'fall11_urls.txt'
	newUrlsFile = outputFolder + '_urlsFullList.txt'

	download_url_list(tarFile, oldUrlsFile, newUrlsFile)
	sample_and_download_imgs(newUrlsFile, N)
	n = clean_corrupted_images()

	while n<N:
		sample_and_download_imgs(newUrlsFile, int(1.5*(N-n)))
		n = clean_corrupted_images()

	remove_url_files(removeTar, tarFile, removeFullList, newUrlsFile)

	print('\nFinished script. Images saved in '+outputFolder+'\n\n')


if __name__ == '__main__':
	main(sys.argv[1:])

