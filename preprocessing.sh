#!/usr/bin/bash
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
python download_sample_images.py 10 Images True True
printf 'PREPROCESSING SAMPLE IMAGES \n'
python process_images.py Images ImagesOut 10 256 256 train

mv ImagesOut/* pix2pix-tensorflow/datasets/imagenet/train
rm -r ImagesOut

printf 'ENUMERATING IMAGES \n'
cd pix2pix-tensorflow/datasets/imagenet/train
counter=0
for file in *; do 
    [[ -f $file ]] && mv -i "$file" $((counter+1)).jpg && ((counter++))
done
