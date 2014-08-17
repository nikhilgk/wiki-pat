#!/bin/bash
source config

rm -rf $PRJROOT/s3/tfidf-op
mkdir $PRJROOT/s3/tfidf-op
cat $PRJROOT/s3/tfidf/* >> $PRJROOT/s3/tfidf-op/tfidf.tsv
echo "OUTPUT FILES AFTER TF-IDF::::::::::::::::::::"

ls -alh $PRJROOT/s3/tfidf-op/