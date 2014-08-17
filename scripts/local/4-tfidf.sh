#!/bin/bash
source config
START=$(date +%s)

rm -rf $PRJROOT/s3/tfidf
python $PRJROOT/python/mr_tfidf.py -r local $PRJROOT/data/$DATAFILE \
	--output-dir=$PRJROOT/s3/tfidf \
    --category_count=$PRJROOT/s3/tfidf-ip/categorycount.tsv \
    --postings_file=$PRJROOT/s3/tfidf-ip/postings.tsv \
    --no-output 

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Execution took $DIFF seconds"
echo "---------------------------------------------"
echo "TF-IDF FILES:::::::::::::::::::::::::::::::::"
ls -al $PRJROOT/s3/tfidf