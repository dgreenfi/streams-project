# Instructions for Infosite and Data Gathering

## Instructions for starting infosite dependencies

### Update Batch Data

####Gather information from Meetup API
python grouplist.py

####Generate static files on top leaders in online communities
python topleaders.py

### Deploy to AWS EC2 Instance
#### Copy all files in folder (requires keyfile)
scp -i {keyfile} -r {yourpath}/streams-project/ ec2-user@ec2-52-91-228-46.compute-1.amazonaws.com:~/


### Activate Services on EC2 Server
#### run from foot base
Setup Redis Server used for front end in the background
redis-server --port 9999 --daemonize yes

#### run from /cred folder
Connect to Twitter and start saving data to redis
nohup python ../streamers/twitter_stream.py &

Start calculating aggregates from Twitter data
nohup python ../streamers/website_processor.py &

#### run from application folder
nohup python application.py &

Site will take 20 minutes from startup to accumulate rolling data for Twitter statistics


## After these commands are run you should be able to navigate to the public url root
http://54.84.155.178:5000/

You should see an app that looks like below:
![alt text][screenshot]

[screenshot]: https://s3.amazonaws.com/dg2815/screenshot_app.png



## Overview of site content
### Background
This page gives background on what we have seen in Colorado and Washington after their legalization of recreational cannabis.
### Legislation
This page gives an overview of legislation that may go to vote in 2016
### Impact
This page projects the financial impact of legislation expected to pass and potentially passing.
### Community Growth
This page shows how online communities have grown as the legalization battle shifted
### Community Leaders
This page highly some key leaders of online communities
### Community Discussion
This page shows real time discussion updates including hashtags, top URLs and volume of conversation on Twitter



