#!/bin/bash
source config
START=$(date +%s)

s3cmd del -r $OUTPUTROOT/postings/
python $PRJROOT/python/mr_postings.py -r emr $INPUTROOT/$DATAFILE \
	--output-dir=$OUTPUTROOT/postings  \
	--no-output \
	--conf-path=$PRJROOT/python/mrjob.conf \
	--pool-emr-job-flows

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Execution took $DIFF seconds"
echo "---------------------------------------------"
echo "POSTINGS FILES:::::::::::::::::::::::::::::::"
s3cmd ls $OUTPUTROOT/postings/