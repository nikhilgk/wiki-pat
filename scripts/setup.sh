mkdir wiki
sudo mount /dev/xvdf wiki
ln -s /mnt src
sudo chown -R ubuntu:ubuntu .
cd src
sudo chown -R ubuntu:ubuntu .
mkdir data
cd data
head -n5000 ~/wiki/rawd/freebase-wex-2009-01-12-articles.tsv > subset.tsv
sudo apt-get update
sudo apt-get -y install python-pip s3cmd
sudo pip install nltk
sudo pip install mrjob
sudo pip install ordereddict
sudo python -m nltk.downloader -d /usr/share/nltk_data all