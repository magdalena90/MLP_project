
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
  imgFiles = [f for f in allFiles if (f.endswith('.jpg') or f.endswith('.png'))]

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


def output_max_class_prob(probs, imgs, labels_idx, outputPath):

  # Create label_probs DataFrame
  label_probs = pd.DataFrame(index=imgs, columns=['maxScore'])

  # Fill DataFrame with max probability
  for i in range(len(probs)):
    selected_probs = [probs[i][j] for j in labels_idx]
    label_probs.loc[imgs[i]] = max(selected_probs)

  # Save DataFrame
  label_probs = label_probs.apply(pd.to_numeric)
  label_probs.sort_index(inplace=True)
  label_probs.to_csv(outputPath)

  return label_probs


def extract_info_from_probs(Class, Model, probs, imgFiles, outputFolder):

  # Get index of selected labels in probs
  file = './selected_synset.txt'
  labels_info = [l.strip() for l in open(file).readlines()]
  labels_info.sort()

  labels = [l.split(' ',1)[0] for l in labels_info if l.split(' ',1)[1]==Class]
  labels_idx = get_labels_idx(labels)

  # RowNames for output DataFrames
  imgs = [i.replace('.jpg','').replace('.png','') for i in imgFiles]
  outputPath = outputFolder+Class+Model+'_probs.csv'

  output_max_class_prob(probs, imgs, labels_idx, outputPath)


def run_model(folder, Class, Model):
  
  batch, imgFiles = get_img_batch(folder + Class+'/'+Model+'/')
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

      class_probs = extract_info_from_probs(Class, Model, probs, imgFiles, folder)


def semantic_classifier(folder):
  Classes = [f for f in os.listdir(folder) if os.path.isdir(os.path.join(folder, f))]
  Models = [f for f in os.listdir(folder+Classes[0]) if os.path.isdir(os.path.join(folder+Classes[0], f))]

  #for Class in Classes:
  #  for Model in Models:
  Class = 'Person'
  Model = 'GeneralModel'
  print '\nRunning classification for Model ' + Model + ' on Class ' + Class + '\n'
  run_model(folder, Class, Model)


def main(args):
  inputFolder = args[0]

  # Hide TensorFlow low level warning
  os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

  # Folders checks
  if not inputFolder.endswith('/'):
      inputFolder += '/'
  
  # Run model and extract probabilities for each class
  semantic_classifier(inputFolder)


if __name__ == '__main__':
  main(sys.argv[1:])
