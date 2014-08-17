#!/bin/bash
source config

rm -rf $PRJROOT/s3/tfidf-ip
mkdir -p $PRJROOT/s3/tfidf-ip/tmp
cd $PRJROOT/s3/tfidf-ip/tmp

s3cmd get -r $OUTPUTROOT/categorycount/part
cat ./* >> categorycount.tsv
s3cmd put categorycount.tsv $OUTPUTROOT/tfidf-ip/categorycount.tsv
mv categorycount.tsv ../
rm *

s3cmd get $OUTPUTROOT/postings/part
cat ./* >> postings.tsv
s3cmd put postings.tsv $OUTPUTROOT/tfidf-ip/postings.tsv
mv postings.tsv ../
# rm *

cd ..
pwd
tar -zcvf tdidip.tar.gz categorycount.tsv postings.tsv
rm -rf tmp
# rm -rf *.tsv

echo "INPUT FILES FOR TF-IDF:::::::::::::::::::::::"
ls -l $PRJROOT/s3/tfidf-ip/