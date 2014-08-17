# rsync -rvtW --delay-updates --modify-window=1 --progress  \
# 	./setupec2.sh $1:/home/ubuntu
rsync -rvtW --delay-updates --modify-window=1 --progress --exclude='data' \
    --exclude='s3' --exclude='part-00000' --exclude='.git' \
	../python ../scripts $1:/home/ubuntu/src
ssh $1  -t "cd /home/ubuntu/src/scripts/emr; bash --login"
