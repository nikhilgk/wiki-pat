#!/bin/bash
source config
START=$(date +%s)

s3cmd del -r $OUTPUTROOT/tfidf/
python $PRJROOT/python/mr_tfidf.py -r emr $INPUTROOT/$DATAFILE \
	--output-dir=$OUTPUTROOT/tfidf \
    --category_count=$OUTPUTROOT/tfidf-ip/categorycount.tsv \
    --postings_file=$OUTPUTROOT/tfidf-ip/postings.tsv \
    --no-output \
	--conf-path=$PRJROOT/python/mrjob.conf \
	--pool-emr-job-flows

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Execution took $DIFF seconds"
echo "---------------------------------------------"
echo "TF-IDF FILES:::::::::::::::::::::::::::::::::"
s3cmd ls $OUTPUTROOT/tfidf/



# python $PRJROOT/python/mr_tfidf.py -r emr $INPUTROOT/$DATAFILE \
# 	--output-dir=$OUTPUTROOT/tfidf \
#     --category_count=$OUTPUTROOT/tfidf-ip/categorycount.tsv \
#     --postings_file=$OUTPUTROOT/tfidf-ip/postings.tsv \
#     ----archive=$PRJROOT/s3/tfidf-ip/tdidip.zip#tfidf-ip
#     --no-output \
# 	--conf-path=$PRJROOT/python/mrjob.conf \
# 	--pool-emr-job-flows