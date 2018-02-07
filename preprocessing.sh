#!/usr/bin/bash

# nImages - number of Images to download
# nTest - number of Images to choose as validation set

nImages=$1
nTest=$2

printf 'CLONNING pix2pix \n'
git clone https://github.com/yenchenlin/pix2pix-tensorflow.git
cd pix2pix-tensorflow
mkdir datasets
cd datasets
mkdir imagenet
cd imagenet
mkdir train
mkdir val
mkdir test

cd ..
cd .. 
cd .. 

printf 'ACTIVATING CONDA ENVIRONMENT \n'
source /home/$USER/miniconda3/bin/activate py27

printf 'DOWNLOADING SAMPLE IMAGES \n'
python download_sample_images.py $nImages Images False False
printf 'PREPROCESSING SAMPLE IMAGES \n'
python process_images.py Images ImagesOut $nImages 256 256 train

mv ImagesOut/* pix2pix-tensorflow/datasets/imagenet/train
rm -r ImagesOut

printf 'ENUMERATING IMAGES \n'
cd pix2pix-tensorflow/datasets/imagenet/train
counter=0
for file in *; do 
    [[ -f $file ]] && mv -i "$file" $((counter+1)).jpg && ((counter++))
done

cd ..
printf 'SELECTING VALIDATION IMAGES \n'
shuf -n $nTest -e train/* | xargs -i mv {} val
printf 'DONE \n'
