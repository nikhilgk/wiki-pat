Setup the datasource on AWS

The data set of interest is here : http://aws.amazon.com/datasets/2345
Documentation here : http://wiki.freebase.com/wiki/WEX/Documentation

To set this on EC2, log on to AWS and go to the EC2 page. 
Change your region to US East/N. Virgina. That is the only region where the the data set volume is available.
Click on Volumes > Create Volume > 
Set size to 80 GB and search for the snapshot id "snap-1781757e". Accept the other defaults
Note the zone where this is created.

Now create a new Instance. Since this is just for the data, t1.micro is sufficient. I used the following AMI image XLT-4.3.4-Java7u21-Ubuntu-13.04-64bit-IPv6 (ami-01061568) since it had Java and Python already on it. When launching make sure this is the same region and zone where the EBS volume was created. Also the default user to SSH intothis one is 'ubuntu' and not 'root'

Once the EC2 instance launcher, go back to the Volume tab and attach the Wikipedia volume to this instance. Subsequently you can SSH to the instance and mount the volume to the instance.

Here are some more details on what you could do with the data: 
https://github.com/utcompling/applied-nlp/wiki/Spark-AWS-Exercise2#create-ebs-volume-with-wikipedia-wex-data-and-attach-it-to-the-cluster
