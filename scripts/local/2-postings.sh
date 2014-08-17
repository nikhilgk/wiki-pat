#!/bin/bash
source config
START=$(date +%s)

rm -rf $PRJROOT/s3/postings
python $PRJROOT/python/mr_postings.py -r local $PRJROOT/data/$DATAFILE \
	--output-dir=$PRJROOT/s3/postings  \
	--no-output


END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Execution took $DIFF seconds"
echo "---------------------------------------------"
echo "POSTINGS FILES:::::::::::::::::::::::::::::::"
ls -al $PRJROOT/s3/postings