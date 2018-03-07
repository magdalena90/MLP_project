#!/usr/bin/bash

# nImages - number of Images to download
# nTest - number of Images to choose as validation set
# nPixel - number of pixels (both width and height) of the images

nImages=$1
nTest=$2
nPixel=$3

printf 'ACTIVATING CONDA ENVIRONMENT \n'
source /home/$USER/miniconda3/bin/activate py27

printf 'DOWNLOADING SAMPLE IMAGES \n'
python download_sample_images.py $nImages Images False False
printf 'PREPROCESSING SAMPLE IMAGES \n'
python process_images.py Images ImagesOut $nImages $nPixel $nPixel train

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
