# sns-boomerang
scheduled sns with aws lambda in a serverless way

swagger: https://0ez607sve0.execute-api.ap-southeast-2.amazonaws.com/dev/doc/

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