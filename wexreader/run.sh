#!/bin/bash

python terms/mr_terms.py ../data/tiny.tsv  --output-dir=./terms  --no-output
python postings_list/mr_postings.py ../data/tiny.tsv  --output-dir=./postings_list  --no-output
python categories/mr_category.py ../data/tiny.tsv  --output-dir=./categories  --no-output

START=$(date +%s)
python classifier/classifier.py ./terms/part-00000 ./postings_list/part-00000 ./categories/part-00000
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "Search took $DIFF seconds"

# [('1819 establishments', 0.2474545190953574), ('Alabama', 0.2474545190953574), ('Confederate states (1861-1865)', 0.2474545190953574), ('Southern United States', 0.2474545190953574), ('States of the United States', 0.17102029619459141)]
