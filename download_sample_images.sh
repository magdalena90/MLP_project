#! bin/bash

# Download tar file with urls and extracts N random lines from file
# If RemoveTar=true, removes tar file, same with RemoveFullList

N=$1
removeTar=$2
removeFullList=$3

mkdir -p Images
cd Images

if [ -f _tarFile.tgz ];then
	printf 'tar file with url list aready exists, skipping download'
else
	printf '\nDownloading list of urls...\n'
	url=http://image-net.org/imagenet_data/urls/imagenet_fall11_urls.tgz
	tarFile=_tarFile.tgz
	wget $url -O $tarFile
fi

if [ -f _urlList.txt ];then
	printf 'tar file already decompressed, skipping decompression'
else
	printf '\nDecompressing tar file...\n'
	tar -zxf $tarFile
	urlFile=_urlList.txt
	mv fall11_urls.txt $urlFile
fi

printf '\nSelecting sample rows...\n'
sampleFile=_urlSublist.txt
shuf -n $N $urlFile > $sampleFile

if [ $removeTar="true" ];then
	printf '\nRemoving tar file\n'
	rm $tarFile
fi

if [ $removeFullList='true' ];then
	printf '\nRemoving full url list file\n'
	rm $urlFile
fi

# Saving images from url
printf '\nDownloading images...\n'
while read l; do
	imgId=$(echo $l | grep -o '^\S*')
	imgUrl=$(echo $l | grep -oP 'http[^ ]+')
	wget -qO "$imgId.jpg" $imgUrl
done < $sampleFile

printf '\n\nFinished. Images saved in ./Images/'

