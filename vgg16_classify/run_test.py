
import sys
import os
import numpy as np
import pandas as pd
import tensorflow as tf
import vgg16
import utils


def get_img_batch(inputFolder):

  # Get files
  allFiles = os.listdir(inputFolder)
  imgFiles = [f for f in allFiles if f.endswith('.jpg')]

  batch = []
  for imgFile in imgFiles:
    img = utils.load_image(inputFolder + imgFile)
    batch.append(img)

  return batch, imgFiles


def get_labels_idx(our_labels):

  # Check that there are no repeated labels in different classes
  if len(our_labels) != len(set(our_labels)):
    print('\nERROR there is at least one label in more than one class\n')

  # Get list of all labels
  all_labels = [l for l in open('./synset.txt').readlines()]
  all_labels = [l.split(' ',1)[0] for l in all_labels]

  # Create list of indices of our_labels in all_labels
  labels_idx = []
  for i in range(len(all_labels)):
    if all_labels[i] in our_labels:
      labels_idx.append(i)

  return labels_idx


def output_labels_probs(probs, imgs, labels, labels_idx, outputFolder):

  # Create label_probs DataFrame
  label_probs = pd.DataFrame(index=imgs, columns=labels)

  # Fill DataFrame with prob of each label
  for i in range(len(probs)):
    selected_probs = [probs[i][j] for j in labels_idx]
    label_probs.loc[imgs[i]] = selected_probs

  # Save DataFrame
  label_probs = label_probs.apply(pd.to_numeric)
  label_probs.to_csv(outputFolder+'img_label_scores.csv')

  return label_probs


def output_img_class(labels_info, imgs, label_probs, outputFolder):
  
  # Get class of each of our labels
  class_dict = {}
  for l in labels_info:
    label, clss = l.split(' ', 1)
    class_dict[label] = clss

  # Determine image class
  max_label = label_probs.idxmax(axis=1)
  max_class = [class_dict[ml] for ml in max_label]

  # Classify anything below 0.1 as Person
  max_prob = label_probs.max(axis=1)
  for i in range(len(max_prob)):
    if max_prob[i] < 0.05:
      max_class[i] = 'Person'
  #for i in range(len(label_probs)):
  #  if max(label_probs[i,:]) < 0.1:
  #    max_class = 'Person'

  # Create img_class DataFrames
  mc_np = np.array(max_class).reshape(len(max_class),1)
  img_class = pd.DataFrame(mc_np, index=imgs, columns=['class'])

  # Save DataFrame
  img_class.to_csv(outputFolder+'img_inferred_class.csv')


def extract_info_from_probs(probs, imgFiles, outputFolder):

  # Get index of selected labels in probs
  file = './selected_synset.txt'
  labels_info = [l.strip() for l in open(file).readlines()]
  labels_info.sort()
  labels = [l.split(' ',1)[0] for l in labels_info]
  labels_idx = get_labels_idx(labels)

  # RowNames for output DataFrames
  imgs = [i.replace('.jpg','') for i in imgFiles]

  label_probs = output_labels_probs(probs, imgs, labels, 
    labels_idx, outputFolder)

  output_img_class(labels_info, imgs, label_probs, outputFolder)


def run_model(inputFolder, outputFolder):
  
  batch, imgFiles = get_img_batch(inputFolder)
  n = len(imgFiles)

  # Run model
  with tf.device('/cpu:0'):
    with tf.Session() as sess:
      images = tf.placeholder('float', [n, 224, 224, 3])
      feed_dict = {images: batch}

      vgg = vgg16.Vgg16()
      with tf.name_scope('content_vgg'):
        vgg.build(images)

      probs = sess.run(vgg.prob, feed_dict=feed_dict)

      extract_info_from_probs(probs, imgFiles, outputFolder)


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
