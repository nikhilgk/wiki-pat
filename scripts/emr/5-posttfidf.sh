#!/bin/bash
source config

rm -rf $PRJROOT/s3/tfidf-op
mkdir $PRJROOT/s3/tfidf-op
cd $PRJROOT/s3/tfidf-op
echo s3cmd get -r $OUTPUTROOT/tfidf/part
s3cmd get -r $OUTPUTROOT/tfidf/part
cat $PRJROOT/s3/tfidf-op/* >> $PRJROOT/s3/tfidf-op/tfidf.tsv
echo "OUTPUT FILES AFTER TF-IDF::::::::::::::::::::"
ls -alh $PRJROOT/s3/tfidf-op/
