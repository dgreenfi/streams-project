# streams-project Code for Infosite and Data Gathering

## Instructions for starting infosite dependencies

### Update Batch Data

####Gather 
python grouplist.py

python topleaders.py

redis-server --port 9999
python twitter_stream.py
python website_processor.py

### Deploy to AWS EC2 Instance

