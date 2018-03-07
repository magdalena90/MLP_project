#!/usr/bin/bash

# nImages - number of Images to download
# nTest - number of Images to choose as validation set
# nPixel - number of pixels (both width and height) of the images

Pix=$1
nImages=$2
nTest=$3
nPixel=$4

if [ $Pix -eq 1 ];then
        printf 'CREATING TRAIN AND VAL FOLDERS FOR pix2pix \n'
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
else
        printf 'SKIPPING CREATING TRAIN AND VAL FOLDERS FOR pix2pix \n'
fi

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
