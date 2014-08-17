#!/bin/bash
source config
START=$(date +%s)

rm -rf $PRJROOT/s3/categorycount
python $PRJROOT/python/mr_categorycounter.py -r local $PRJROOT/data/$DATAFILE \
	--output-dir=$PRJROOT/s3/categorycount  \
	--no-output


END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Execution took $DIFF seconds"
echo "---------------------------------------------"
echo "CATEGORY COUNT:::::::::::::::::::::::::::::::"
cat $PRJROOT/s3/categorycount/part-00000