#!/bin/bash
# recognizing scans by tesseract and cleaning and converting to txt
for file in $(ls *jpg | sort -t'-' -nk2.1) #sorting files by number
do
	echo "working with $file"
	filename="${file%%.*}"
	tesseract -l ukr+eng+rus $file $filename --psm 6 #tesseract scan every jpg file and convert to txt with columns
	#tesseract -l ukr $file $filename #simple recognition
	# first sed - remove quotes; 2) remove |; 3) remove blank lines; 4) remove spaces between letters; 4) gawk replace spaces with 5) adding to file
	#sed "s/['\"]//g" $filename.txt | sed 's/|//g' | sed '/^$/d' | sed '{ s/\([а-яА-Я]\) \([а-яА-Я]\)/\1_\2/g}' | gawk 'BEGIN{OFS=";"}; {$1=$1;print $0}' >> scheme_final.csv
	sed 's/|//g' $filename.txt | sed "s/['\"]//g" >> text_$(date +%y-%m-%d_%H-%M).txt
	rm $filename.txt
done
cp text_$(date +%y-%m-%d_%H-%M).txt ../text_$(date +%y-%m-%d_%H-%M).txt
echo "File text_$(date +%y-%m-%d_%H-%M).txt copied to $(readlink -f ../)"