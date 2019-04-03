# sns-boomerang
in the event sourcing world, if we can contorl (schedule) the events, then we can schedule our applications invocaltion.

sns-boomerang schedules sns in a serverless fashion.

![boomerang](boomerang.png)

# SETUP
## dependency:
before you start  
`pip install tox`  
run command (install dev dependency)  
`tox -e dev`  
install dependency  
`pip install -r requirements.txt`

# RUN CODE  
`python app.py`

# SWAGGER  
`http://127.0.0.1:5000/doc`  

# Deploy 
`zappa deploy`  
more on zappa checkout: https://github.com/Miserlou/Zappa

# Reference
https://docs.aws.amazon.com/amazondynamodb/latest/APIReference/API_Operations_Amazon_DynamoDB_Streams.html  
https://aws.amazon.com/sns/  
https://aws.amazon.com/sqs/  
https://aws.amazon.com/lambda/  