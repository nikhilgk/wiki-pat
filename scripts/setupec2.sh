rsync -rvtW --delay-updates --modify-window=1 --progress  \
	./setup.sh $1:/home/ubuntu
ssh $1 -t "/home/ubuntu/setup.sh; bash --login"