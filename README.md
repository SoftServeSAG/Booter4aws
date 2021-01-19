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




## Package description
#### cr2_control
Package for launching cr2 robot
#### robot_monitoring
Package for publishing different metrics(e.g. distance to the goal) to ros topics.


## Run CR2 Single robot
To run single Catering Robot you need to run following command:
```
./setup/aws_setup.bash start_single_robot.json
```
During the first run it creates AWS infrustructure, copies bundle to the s3 bucket and runs simulation application.


## Run CR2 Fleet

To run fleet on AWS Robomaker
```
./setup/aws_setup.bash start_four_robots.json 
```

If AWS stack was not created before, script will create it.


### Typical config to launch fleet 

```json
{
    "robots": [
        {
        "name": "robot1",
        "environmentVariables": {
            "START_X": "2",
            "START_Y": "2",
            "START_Z": "0.0",
            "START_YAW": "0",
            "USE_CUSTOM_MOVE_OBJECT_GAZEBO_PLUGIN":"true",
            "MAPPING":"false",
            "ROBOT_MONITORING":"true",
            "ROBOT_TESTING":"false"
        },
        "packageName": "cr2_control",
        "launchFile": "cr2_fleet.launch"
        }
      
    ],
    "server": {
        "name": "SERVER",
        "environmentVariables": {
            "START_X": "0",
            "START_Y": "1",
            "START_Z": "0.0",
            "START_YAW": "0",
            "USE_CUSTOM_MOVE_OBJECT_GAZEBO_PLUGIN":"true",
            "MAPPING":"false",
            "ROBOT_MONITORING":"true",
            "ROBOT_TESTING":"false"
        },
        "packageName": "cr2_control",
        "launchFile": "cr2_fleet.launch"
      }

  }
```

There are several environment variables to configure simulation:
1. MAPPING - enable mapping using gmapping and explore_lite, default - false
2. ROBOT_MONITORING - enable robot monitoring, default - false 
3. ROBOT_TESTING - run tests (on current version simple navifation test), default - false


## CICD
This repository is ready for AWS CICD using AWS Pipelines

Steps to configure CICD:
1. Create AWS stack
```
./setup/aws_setup_cicd.bash 
```
This script will create two stacks: first contains only bucket for storing bundles and AWS lamdas sources. The second stack creates all needed infrustructure for running simulation jobs.
2. Update build file buildspec.yml with your S3Bucket name received in first step, so build machine will know where bundle should be located
```
    S3_BUCKET: <YOUR-BUCKET>
```
3. All further instructions how to configure AWS CICD Pipeline you can find here https://github.com/aws-samples/aws-robomaker-simulation-launcher

Note! Build role must have next access to the S3Bucket or use one created by cloudformation(name contains CodeBuildRole)
```
        {
            "Effect": "Allow",
            "Resource": [
                "arn:aws:s3:::<YOUR-BUCKET>/*"
            ],
            "Action": [
                "s3:PutObject",
                "s3:GetObject",
                "s3:GetObjectVersion",
                "s3:GetBucketAcl",
                "s3:GetBucketLocation"
            ]
        }
```

You can configure CICD scenarios in file "scenarios.json" 


## Cleanup

To delete the sample application use the AWS CLI.

For Fleet application
```
aws cloudformation delete-stack --stack-name r2-robomaker-fleet
```
For CICD
```
aws cloudformation delete-stack --stack-name r2-robomaker-fleet-cicd
aws cloudformation delete-stack --stack-name r2-robomaker-fleet-cicd-bucket
```