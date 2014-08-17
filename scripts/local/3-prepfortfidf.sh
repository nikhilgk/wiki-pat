#!/bin/bash
source config

rm -rf $PRJROOT/s3/tfidf-ip
mkdir $PRJROOT/s3/tfidf-ip
cat $PRJROOT/s3/categorycount/* >> $PRJROOT/s3/tfidf-ip/categorycount.tsv
cat $PRJROOT/s3/postings/* >> $PRJROOT/s3/tfidf-ip/postings.tsv
echo "INPUT FILES FOR TF-IDF:::::::::::::::::::::::"

ls -alh $PRJROOT/s3/tfidf-ip/