   _____  __      __  _________ __________      ___.             _____          __                 
  /  _  \/  \    /  \/   _____/ \______   \ ____\_ |__   ____   /     \ _____  |  | __ ___________ 
 /  /_\  \   \/\/   /\_____  \   |       _//  _ \| __ \ /  _ \ /  \ /  \\__  \ |  |/ // __ \_  __ \
/    |    \        / /        \  |    |   (  <_> ) \_\ (  <_> )    Y    \/ __ \|    <\  ___/|  | \/
\____|__  /\__/\  / /_______  /  |____|_  /\____/|___  /\____/\____|__  (____  /__|_ \\___  >__|   
        \/      \/          \/          \/           \/               \/     \/     \/    \/       
 ----------------------------------------------------------------- 

The IAM user needs read and write permissions to several services, including provisioning resources with AWS CloudFormation, AWS RoboMaker, Amazon S3, AWS Cloud9, Amazon CloudWatch, Amazon VPC, AWS Lambda and AWS Identity and Access Management. 
Please make sure you have these permissions in your account before proceeding further.


This description is valid for AWS Robomaker Cloud9 IDE and it is not tested locally(could work with minor changes)


# Description

This repository is created to demonstarte CR2 robot on AWS Robomaker.


## Initial ROS setup
1. Download this repository 
2. Go to downloaded folder and run `./setup/ros_setup.bash`
It downloads all needed ROS dependencies and builds all ROS packages


## Run CR2 Single robot
TODO




## Run CR2 Fleet

To run fleet on AWS Robomaker





## CICD
This repository is ready for AWS CICD using AWS Pipelines
See details here https://github.com/aws-samples/aws-robomaker-simulation-launcher

TODO: describe stack creation with lambdas()




##Cleanup

To delete the sample application and the bucket that you created, use the AWS CLI.

aws cloudformation delete-stack --stack-name cr2-robomaker
aws s3 rb s3://BUCKET_NAME