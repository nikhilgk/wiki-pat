## Sumary of steps:

1. Clone the code to your local computer
2. Inital setup in aws.amazon.com to setup your 'base' instance from where you will launch the emr map reduce activities
3. Sync your local repo with the 'base' instance
4. During dev use the scripts in scripts/local to launch your jobs (This can be done from local machine or 'base' instance)
5. For production run or testing with hadoop/emr, use the scripts in scripts/emr

##Detailed Instructions


###From aws.amazon.com, 
- Create a volume from 'snap-1781757e' . This will be created in the us-east-1d region
- Create a 'c3.large' ec2 instance in the us-east-1d region using 'Ubuntu Server 14.04 LTS (HVM), SSD Volume Type - ami-864d84ee'
- Attach the volume created above to this instance at the mount point '/dev/sdf'

###In your local machine,
- Install rsync
- Install the private key from aws so that rsync and ssh can work without being prompted for keys

    `ssh-add <PATH TO LOCAL LOCATION OF AWS KEY.pem FILE>`
- Copy your private key to 'base' instance as well. 

	`scp <PATH TO LOCAL LOCATION OF AWS KEY.pem FILE> ubuntu@<SERVER HOST NAME  IP>:~/.ssh/key.pem`
- Update configurations in `python/mrjob.conf` with your credentials

###To prep and sync code with the aws instance 
- From a terminal, go to the scripts directory and execute

	`./setupec2.sh ubuntu@<AWS DNS NAME OR IP>`

    This will install mrjob, python etc on the 'base' instance
    
- Once setup of the ec2 instance is completed, run the following command and provide your AWS credentials

	`s3cmd --configure`

- Anytime you make a change to local file and need to sync it to the ec2 instance, execute   

	`./syncec2.sh ubuntu@<AWS DNS NAME OR IP>`

##Scripts
####config
- Configure the name and location of input data
- Configure the location of the output data

####0-setup.sh
- Clears the output folder 

####1-catecorycount.sh
- Runs the category counter and stores output in <outputlocation>/categorycount/

####2-postings.sh
- Generate the summary postings files and stores output in <outputlocation>/postings/

####3-prepfortfidf.sh
- Consolidates the ooutput files from 1 and 2 and prepares for next step

####4-tfidf.sh
- Generates the tfidf and stores it in <outputlocation>/tfidf/

####5-posttfidf.sh
- Stores the tfidf data into the elasticcache <Work in progress>

