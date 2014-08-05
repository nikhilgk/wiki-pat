#!/bin/bash
START=$(date +%s)

python mr_categories.py ../data/subset.tsv --output-dir=./categories  --no-output

python mr_postings.py ../data/subset.tsv --output-dir=./postings  --no-output

python mr_terms.py ../data/subset.tsv --output-dir=./terms --postings_file=./postings/part-00000 --no-output --category_count=./categories/part-00000 

END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Indexing took $DIFF seconds"
echo "---------------------------------------------"
ls -lh  ./terms/

START=$(date +%s)
python search.py ./terms/part-00000 ./postings/part-00000 ./categories/part-00000 
END=$(date +%s)
DIFF=$(( $END - $START ))
echo "---------------------------------------------"
echo "Search took $DIFF seconds"
echo "---------------------------------------------"
