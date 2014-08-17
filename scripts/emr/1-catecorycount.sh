#!/bin/bash
source config
START=$(date +%s)

s3cmd del $OUTPUTROOT/categorycount/
python $PRJROOT/python/mr_categorycounter.py -r emr $INPUTROOT/$DATAFILE \
	--output-dir=$OUTPUTROOT/categorycount  \
	--no-output \
	--conf-path=$PRJROOT/python/mrjob.conf \
	--pool-emr-job-flows


END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Execution took $DIFF seconds"
echo "---------------------------------------------"
echo "CATEGORY COUNT:::::::::::::::::::::::::::::::"
s3cmd ls $OUTPUTROOT/categorycount/