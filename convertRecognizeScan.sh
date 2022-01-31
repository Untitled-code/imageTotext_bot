#!/bin/bash

echo "Starting bash script and working with dir $(pwd)"
ls
for file in *.pdf
do
	echo "Name of file: $file" 
	dir=$(dirname "$file") #get dirname from path
	filewithoutext="${file%%.*}" #get filename without extension
	newDir=$filewithoutext$(date +%y-%m-%d_%H-%M)
	filename=$(basename $file) #parse file from full path
	cd $dir
	mkdir $newDir
	echo "New directory $newDir is made"
	cp ./$filename $newDir/
	cd $newDir
	echo "Making $newDir and copying target file $filename"
	#convert-im6.q16 ./$filename page.jpg
	convert-im6.q16 -density 300 ./$filename p.jpg
	#convert -density 150 ./$filename -depth 8 -background white page.tiff #convert to tiff
	#echo "converting is completed. Starting python script"
	#/home/investigator/NAS/Oleg_NAS/scripts3/WebScrapingWIthPython/mine/textRecognition/imageToString.py
	echo "starting tesseract with scanAndClean.sh"
	../../scanAndClean.sh
	rm *.jpg
	rm *pdf
	echo "Done with $file"
done
echo "Done!"
