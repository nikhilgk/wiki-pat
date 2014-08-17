#!/bin/bash
source config
s3cmd del -r $OUTPUTROOT
# cd $PRJROOT/python
# pwd
# python -m mrjob.tools.emr.create_job_flow --conf-path=$PRJROOT/python/mrjob.conf
